import java.io.*;
import java.net.*;
import java.util.*;

public class Bank {
    private ServerSocket ss;
    private Socket s;
    private PrintWriter outStream;
    private ObjectInputStream objectIn;
    private ObjectOutputStream objectOut;
    private HashMap<String, ArrayList<String>> accounts;
    private int d,  // private key
    e,  // public key
    n,  // mod n
    atmE,
    atmN;

    public Bank() {
        try {
            ss = new ServerSocket(4999);
            s = ss.accept();
            outStream = new PrintWriter(s.getOutputStream());
            objectOut = new ObjectOutputStream(s.getOutputStream());
            objectIn = new ObjectInputStream(s.getInputStream());
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        fillAccounts();
    }

    private void fillAccounts() {
    	this.accounts  = new HashMap<String, ArrayList<String>>();
    	
    	ArrayList<String> list = new ArrayList<String>(2);
    	list.add("Abdul Razzak");
    	list.add("1000");
    	this.accounts.put("12345678", list);
    	
    	list = new ArrayList<String>(2);
    	list.add("John");
    	list.add("100");
    	this.accounts.put("12345670", list);
    }
    
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Bank session = new Bank();
        
        int [] keyPairs = RSA.generateKeyPairs();
        session.n = keyPairs[0];
        session.d = keyPairs[1];
        session.e = keyPairs[2];

        session.setUpConnection();
        
        System.out.println("ATM connected");
        
        List<Integer> c = (List<Integer>) session.objectIn.readObject();
        String clientInput;
        String currentCard = "";
        int clientInputNum = Integer.parseInt(RSA.decipher(c, session.d, session.n));

        while (clientInputNum != 7) {
            if (clientInputNum == 0) {
                c = (List<Integer>) session.objectIn.readObject();
                clientInput = RSA.decipher(c, session.d, session.n);
                currentCard = clientInput;
                System.out.println("curentCard = " + currentCard);
            }
            else if (clientInputNum == 1) {
                c = (List<Integer>) session.objectIn.readObject();
                clientInput = RSA.decipher(c, session.d, session.n);
                if (session.accounts.containsKey(clientInput)) {
                    session.outStream.println("true");
                    session.outStream.flush();
                }
                else {
                    session.outStream.println("false");
                    session.outStream.flush();
                }
            }
            else if (clientInputNum == 2) {
                clientInput = session.accounts.get(currentCard).get(1);
                c = RSA.getCipher(clientInput, session.atmE, session.atmN);
                session.objectOut.writeObject(c);
                session.objectOut.flush();
            }
            else if (clientInputNum == 3) {
                clientInput = session.accounts.get(currentCard).get(0);
                c = RSA.getCipher(clientInput, session.atmE, session.atmN);
                session.objectOut.writeObject(c);
                session.objectOut.flush();
            }
            else if (clientInputNum == 4) {
                c = (List<Integer>) session.objectIn.readObject();
                clientInput = RSA.decipher(c, session.d, session.n);
                double withdraw = Double.parseDouble(clientInput);

                clientInput = session.accounts.get(currentCard).get(1);
                double balance = Double.parseDouble(clientInput);
                balance -= withdraw;
                session.accounts.get(currentCard).set(1, Double.toString(balance));
            }
            else if (clientInputNum == 5) {
                c = (List<Integer>) session.objectIn.readObject();
                clientInput = RSA.decipher(c, session.d, session.n);
                double withdraw = Double.parseDouble(clientInput);

                clientInput = session.accounts.get(currentCard).get(1);
                double balance = Double.parseDouble(clientInput);
                balance += withdraw;
                session.accounts.get(currentCard).set(1, Double.toString(balance));
            }
            else if (clientInputNum == 6) {
                currentCard = "";
            }
            c = (List<Integer>) session.objectIn.readObject();
            clientInputNum = Integer.parseInt(RSA.decipher(c, session.d, session.n));
        }
        session.s.close();
        session.ss.close();
    }

    private void setUpConnection() {
        int pms = 0;
        String bankRand;

        this.outStream.println(this.e);
        this.outStream.println(this.n);
        this.outStream.flush();

        try {
            this.atmE = Integer.parseInt(RSA.decipher((List<Integer>) objectIn.readObject(), d, n));
            this.atmN = Integer.parseInt(RSA.decipher((List<Integer>) objectIn.readObject(), d, n));
            pms = Integer.parseInt(RSA.decipher((List<Integer>) objectIn.readObject(), d, n));
            Random random = new Random(pms);
            bankRand = random.nextInt() + "";
            this.objectOut.writeObject(RSA.getCipher(bankRand, atmE, atmN));
            this.objectOut.flush();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void printCipher(List<Integer> c) {
        System.out.print("Cipher = ");
        for (Integer i : c) {
            System.out.print(i);
        }
        System.out.println();
    }
}