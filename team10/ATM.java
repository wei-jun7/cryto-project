import java.io.*;
import java.net.*;
import java.util.*;
import java.security.*;

public class ATM {
    private static Scanner keyBoard;
    private Socket s;
    private PrintWriter outStream;
    private ObjectOutputStream objectOut;
    private BufferedReader inputStream;
    private ObjectInputStream objectIn;
    private SecureRandom pms;
    private int e, d, n;
	 private int bankE;
	 private int bankN;

    public ATM() {
        try {
            keyBoard = new Scanner(System.in);
            s = new Socket("localhost", 4999);
            outStream = new PrintWriter(s.getOutputStream());
            objectOut = new ObjectOutputStream(s.getOutputStream());
            inputStream = new BufferedReader(new InputStreamReader(s.getInputStream()));
            objectIn = new ObjectInputStream(s.getInputStream());
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        pms = new SecureRandom();
    }
    private void depositCash() {
        System.out.print("Please enter a deposit amount: ");
        double deposit = keyBoard.nextDouble();
        keyBoard.nextLine();
        
        while (true) {
              if (deposit < 0) {
                 System.out.print("Please enter a correct amount: ");
                 deposit = keyBoard.nextDouble();
                 keyBoard.nextLine();
              }
              else {
                 break;
              }
        }
        try {
           List<Integer> c = RSA.getCipher("5", this.bankE, this.bankN);
           this.objectOut.writeObject(c);
           this.objectOut.flush();
           
           String cipher = deposit + "";
           c = RSA.getCipher(cipher, this.bankE, this.bankN);
           this.objectOut.writeObject(c);
           this.objectOut.flush();
        }
        catch (Exception e) {
           e.printStackTrace();
        }
    }
    
    private void endUser() {
         try {
            List<Integer> c = RSA.getCipher("6", this.bankE, this.bankN);
            this.objectOut.writeObject(c);
            this.objectOut.flush();
         }
         catch (Exception e) {
            e.printStackTrace();
         }
    }

    private int generatePMS() {
        pms.setSeed(pms.generateSeed(2));
        int random = pms.nextInt();
        if (random < 0) {
            return (random*(-1));
        }
        else {
            return random;
        }
    }
    
    private double getUserBalance() {
        List<Integer> c = new LinkedList<Integer>();
        try {
           c = RSA.getCipher("2", bankE, bankN);
           objectOut.writeObject(c);
           objectOut.flush();
           
           c = (List<Integer>) objectIn.readObject();
         }
         catch(Exception e) {
            e.printStackTrace();
         }

        return Double.parseDouble(RSA.decipher(c, this.d, this.n));
    }

    private String getUserName() {
        List<Integer> c = new LinkedList<Integer>();
        try {
           c = RSA.getCipher("3", bankE, bankN);
           objectOut.writeObject(c);
           objectOut.flush();
           
           c = (List<Integer>) objectIn.readObject();
         }
         catch (Exception e) {
            e.printStackTrace();
         }
        
        return RSA.decipher(c, this.d, this.n);
    }
    

    private int printMenu() {
        System.out.println("Please press a number to perform its corresponding operation (press q to exit)");
        System.out.println("1. Withdraw Cash\n2. Make Deposit");
        String userInput = keyBoard.nextLine();

        while (true) {
            if (userInput.equals("1"))
                return 1;
            else if (userInput.equals("2"))
                return 2;
            else if (userInput.toLowerCase().equals("q"))
                return 3;
            else {
                System.out.println("Please press a number to perform its corresponding operation (press q to exit)");
                System.out.println("1. Withdraw Cash\n2. Make Deposit");
                userInput = keyBoard.nextLine();
            }
        }
    }
    
    private boolean setUser(String cardNum) {
      List<Integer> c = RSA.getCipher("0", bankE, bankN);
      try {
         objectOut.writeObject(c);
         objectOut.flush();
         
         c = RSA.getCipher(cardNum, bankE, bankN);
         objectOut.writeObject(c);
         objectOut.flush();
      }
      catch (Exception e) {
         e.printStackTrace();
      }
      return true;
    }

    private boolean verifiedCardNumber(String cardNumber) throws IOException {
        List<Integer> c = RSA.getCipher("1", bankE, bankN);
        objectOut.writeObject(c);
        objectOut.flush();
        
        c = RSA.getCipher(cardNumber, bankE, bankN);
        objectOut.writeObject(c);
        objectOut.flush();

        try {
            if (inputStream.readLine().equals("true")) {
               return true;
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        
        return false;
    }

    private void withdrawCash(double balance) {
        if (balance <= 0) {
            System.out.println("Balance not sufficient for withdrawal!");
        }
        else {
            System.out.print("Please enter a withdrawal amount: ");
            double withdraw = keyBoard.nextDouble();
            keyBoard.nextLine();
            
            while (true) {
               if (withdraw > balance || withdraw < 0) {
                  System.out.print("Please enter a correct amount: ");
                  withdraw = keyBoard.nextDouble();
                  keyBoard.nextLine();
               }
               else {
                  break;
               }
            }
            try {
               List<Integer> c = RSA.getCipher("4", this.bankE, this.bankN);
               this.objectOut.writeObject(c);
               this.objectOut.flush();
               
               String cipher = withdraw + "";
               c = RSA.getCipher(cipher, this.bankE, this.bankN);
               this.objectOut.writeObject(c);
               this.objectOut.flush();
            }
            catch (Exception e) {
               e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws IOException {
        ATM atm = new ATM();
        
        int[] keyPairs = RSA.generateKeyPairs();
        atm.n = keyPairs[0];
        atm.d = keyPairs[1];
        atm.e = keyPairs[2];

        int preMaster = atm.generatePMS();
        atm.setUpConnection(preMaster);

        String userInput;
        String userName;
        
        double userBalance;

        System.out.print("Welcome to Bank of America\nPlease enter your card number (press q to quit): ");
        userInput = keyBoard.nextLine();
        
        while (!userInput.toLowerCase().equals("q")) {
            if (atm.verifiedCardNumber(userInput)) {
                atm.setUser(userInput);
                userName = atm.getUserName();
                userBalance = atm.getUserBalance();
                System.out.printf("Welcome %s \nBalance: $%.2f\n", userName, userBalance);
                int menu = atm.printMenu();
                while (true) {
                    if (menu == 1) {
                        atm.withdrawCash(userBalance);
                        userBalance = atm.getUserBalance();
                        System.out.printf("Balance: $%.2f\n", userBalance);
                    }
                    else if (menu == 2) {
                        atm.depositCash();
                        userBalance = atm.getUserBalance();
                        System.out.printf("Balance: $%.2f\n", userBalance);
                    }
                    else if (menu == 3) {
                        atm.endUser();
                        break;
                    } 
                    menu = atm.printMenu();
                }
            }
            else {
            	System.out.println("Card number does not exist");
            }
            System.out.print("Welcome to Bank of America\nPlease enter your card number (press q to quit): ");
            userInput = keyBoard.nextLine();
        }
        List<Integer> c = RSA.getCipher("7", atm.bankE, atm.bankN);
        atm.objectOut.writeObject(c);
        atm.objectOut.flush();
        atm.s.close();
        System.out.println("Thankyou for using Bank of America! We hope to see you again");
    }

    private void setUpConnection(int pms) {
        try {
            List<Integer> bankCipher;
            String bankRand;

            this.bankE = Integer.parseInt(inputStream.readLine());
            this.bankN = Integer.parseInt(inputStream.readLine());

            RSA.generateKeyPairs();

            //Send ATM public and private keys
            objectOut.writeObject(RSA.getCipher(this.e + "", this.bankE, this.bankN));
            objectOut.writeObject(RSA.getCipher(this.n + "", this.bankE, this.bankN));

            //Send PMS
            objectOut.writeObject(RSA.getCipher(pms + "", this.bankE, this.bankN));
            objectOut.flush();

            Random random = new Random(pms);
            String atmRand = random.nextInt() + "";
            bankCipher = (List<Integer>) objectIn.readObject();
            bankRand = RSA.decipher(bankCipher, this.d, this.n);
            if (!bankRand.equals(atmRand)) {
                System.out.println("Connection not Verified!");
                System.exit(0);
            }
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
