import java.util.*;

public class RSA {
	private static HashSet<Integer> prime = new HashSet<>();
    private static Random random = new Random();
	
    // public static void main(String[] args) {
	// 	primeFiller();
	// 	String message = "Intagraamaekna msdn";
        
    //     int[] keys = RSA.generateKeyPairs();
    //     int n = keys[0];
    //     int d = keys[1];
    //     int e = keys[2];

    //     List<Integer> c = RSA.getCipher(message, e, n);
    //     //System.out.println(c);
    //     System.out.println(RSA.decipher(c, d, n));

	// 	// Uncomment below for manual input
	// 	// System.out.println("Enter the message:");
	// 	// message = new Scanner(System.in).nextLine();

	// 	//List<Integer> coded = encoder(message);

	// }

	private static void primeFiller() {
		boolean[] primeArr = new boolean[250];
		for (int i = 0; i < 250; i++)
			primeArr[i] = true;

		primeArr[0] = false;
		primeArr[1] = false;

		for (int i = 2; i < 250; i++)
			for (int j = i * 2; j < 250; j += i)
				primeArr[j] = false;

		for (int i = 0; i < primeArr.length; i++)
			if (primeArr[i])
				prime.add(i);
	}

	private static int pickRandomPrime() {
		int k = random.nextInt(prime.size());
		List<Integer> primeList = new ArrayList<>(prime);
		int randomPrime = primeList.get(k);
		prime.remove(randomPrime);
		return randomPrime;
	}

	public static int[] generateKeyPairs() {
        primeFiller();
		int rand1 = pickRandomPrime();
		int rand2 = pickRandomPrime();

		int n = rand1*rand2;
		int phi = (rand1-1)*(rand2-1);

		int e = 2;
		while (true) {
			if (gcd(e, phi) == 1) {
				break;
			}
			e += 1;
		}

		int d = 2;
		while (true) {
			if ((d * e) % phi == 1) {
				break;
			}
			d += 1;
		}

        int[] keyPairs = new int[3];
        keyPairs[0] = n;
        keyPairs[1] = d;
        keyPairs[2] = e;

        return keyPairs;
	}

	private static int encrypt(int message, int e, int n) {
		int txt = 1;
		while (e > 0) {
			txt *= message;
			txt %= n;
			e -= 1;
		}
		return txt;
	}

	private static int decrypt(int cipher, int d, int n) {
		int decipherNum = 1;
        while (d > 0) {
            decipherNum *= cipher;
            decipherNum %= n;
            d -= 1;
        }
		return decipherNum;
	}

	private static int gcd(int a, int b) {
		if (b == 0) {
			return a;
		}
		return gcd(b, a % b);
	}

	public static List<Integer> getCipher(String message, int e, int n) {
		List<Integer> encoded = new ArrayList<>();
		for (char letter : message.toCharArray()) {
			encoded.add(encrypt((int)letter, e, n));
		}
		return encoded;
	}

	public static String decipher(List<Integer> encoded, int d, int n)
	{
		StringBuilder s = new StringBuilder();
		for (int num : encoded) {
			s.append((char)decrypt(num, d, n));
		}
		return s.toString();
	}
}
