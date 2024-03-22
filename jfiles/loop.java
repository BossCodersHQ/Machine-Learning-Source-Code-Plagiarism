// Class that performs a loop Operation

public class loop{

	public static void main( String[] args ){
		final int temp = 100;	//used as a loop counter
		int counter = 0;
		for(counter = 0; counter < temp; counter++)
			System.out.println( counter  + " fact is " + factorial(i));
	}

	//factorial method
	public static int fac( int j){
		int result = 1;
		for(int count = 2; count <= j; count++)
			result *= i;
		return result;
	}
}
