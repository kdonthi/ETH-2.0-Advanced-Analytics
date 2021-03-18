class listplusN {
	public int[]	list;
	public int	mse;
}

class Array {
	public static int[] slices(int[] array, int si, int ei) { 
		//Returns the element in array1 from indices si to ei, inclusive.
		int newarraylen = (ei - si) + 1;
		int newarray[] = new int[newarraylen];
		int counter = 0;
		for (int i = si; i <= ei; i++) {
			newarray[counter++] = array[i];
		}
		return (newarray);
	}
	public static int[] concat(int[] array1, int[] array2) {
		int newarraylen = array1.length + array2.length;
		int newarray[] = new int[newarraylen];
		int index = 0;
		for (int i = 0; i < array1.length; i++)
		{
			newarray[index++] = array1[i];
		}
		for (int i = 0; i < array2.length; i++)
		{
			newarray[index++] = array2[i];
		}
		return newarray;
	}
	public static void printarray(int[] array) {
		for (int i = 0; i < array.length; i++)
		{
			System.out.printf("%d ",array[i]);
		}
		System.out.println();
	}
	public static int[] arrcpy(int[] src)
	{
		int newarray[] = new int[src.length];
		for (int i = 0; i < src.length; i++)
			newarray[i] = src[i];
		return (newarray);
	}
	public static int straighttoend(int[] array, int lastindex) {
		int i = array[0];
		int index = 0;
		while(index <= lastindex) {
			if (i++ != array[index++])
				return (0);
		}
		return (1);
	}	
}
public class optimalSubsample {
	public static int square(int number) {
		return (number * number);
	}
	public static int mse(int[] ia, int optimaldiff, int[] original) {
		int error = 0;
		//Array.printarray(original);
		for (int i = 0; i < (ia.length - 1); i++)
		{ 
			//System.out.println(i);
			error += square(original[ia[i + 1]] - original[ia[i]]) - optimaldiff;
		}
		return (error);
	}
	public static listplusN recur(int[] list, int N, int[] original, int optimaldiff, listplusN[][] indbyN) {
		listplusN obj = new listplusN();
		int[] rtrnarray;
		int length = list.length;
		if (N == 2) //if we only have to choose two numbers, just choose begin and end
		{
			rtrnarray = new int[2];
			rtrnarray[0] = list[0];
			rtrnarray[1] = list[length - 1];
			obj.list = rtrnarray;
			obj.mse  = mse(rtrnarray, optimaldiff, original);;
			return (obj);
		}
		else if (list.length == N) { //if N == length of the list, return the whole list
			obj.list = Array.arrcpy(list);
			obj.mse = mse(list, optimaldiff, original);
			return (obj);
		}
		else if (Array.straighttoend(list, list.length - 1) == 1) {
			if (indbyN[list[0]][N-1] != null) {
				return (indbyN[list[0]][N-1]);
			}
		}

		//When including a number, it is the same as recur({0, list[1]}, 2) + recur({list[1] -> list[len-1], 2})
		listplusN rtrn1a = recur(Array.slices(list, 0, 1), 2,  original, optimaldiff, indbyN);
		listplusN rtrn1b = recur(Array.slices(list, 1, list.length - 1), N - 1, original, optimaldiff, indbyN);
		int[] removedindex = Array.concat(Array.slices(list, 0, 0), Array.slices(list, 2, list.length - 1)); //removing the number at first index
		listplusN rtrn2 = recur(removedindex, N, original, optimaldiff, indbyN);
		int firstindex = 0;
		int[] rtrn1bfirstrem;
		int[] conc;

		if (rtrn1a.mse == -1 || rtrn1b.mse == -1)
			return (rtrn2);
		else if (rtrn2.mse == -1)
			return (rtrn1a);
		else if (rtrn1a.mse + rtrn1b.mse < rtrn2.mse) {
				rtrn1bfirstrem = Array.slices(rtrn1b.list, 1, (rtrn1b.list).length - 1);
				obj.list = Array.concat(rtrn1a.list, rtrn1bfirstrem);
				obj.mse = rtrn1a.mse + rtrn1b.mse;
				if (Array.straighttoend(list, list.length - 1) == 1 && indbyN[list[0]][N-1] == null)
						indbyN[list[0]][N-1] = obj;
				
		}
		else if (rtrn1a.mse + rtrn1b.mse >= rtrn2.mse) {
			obj.list = Array.arrcpy(rtrn2.list);
			obj.mse = rtrn2.mse;
			if (Array.straighttoend(list, list.length - 1) == 1 && indbyN[list[0]][N-1] == null)
				indbyN[list[0]][N-1] = obj;
		}
		return (obj);
			
	}

	public static int[] optimalSubsample(int[] array, int N) {
		if (N < 2) {
			System.out.println("Make sure you are choosing N greater than or equal to 2.");
			System.exit(1);
		}
		
		if (N > array.length) {
			System.out.printf("Make sure your N is not greater than the amount of elements in the array!%n Your N is %d and your array length is %d.%n", N, array.length);
			System.exit(1);
		}

		int[] returnlist;
		if (N == 2) {
			returnlist = new int[2];
			returnlist[0] = array[0];
			returnlist[1] = array[1];
			return (returnlist);
		}

		if (N == array.length) {
			return (array);
		}
		int optimaldiff = (array[array.length - 1] - array[0]) / (N-1);
		listplusN[][] indexbyN = new listplusN[array.length][N];
		int[] indexarray = new int[array.length];
		for (int i = 0; i < array.length; i++)
			indexarray[i] = i;
		listplusN[][] arrayindexbyN = new listplusN[array.length][N];
		int[] finalia = recur(indexarray, N, array, optimaldiff, arrayindexbyN).list;
		returnlist = new int[finalia.length];
		for (int i = 0; i < finalia.length; i++)
		{
			returnlist[i] = array[finalia[i]]; //converting indexes into numbers
		}

		return (returnlist);
	}

	public static void main (String[] args) {
		int array1[] = {0, 33, 50, 66, 100};
		int array2[] = new int[100];
		for (int i = 0; i < 100; i++) {
			array2[i] = i;
		}
		int array3[] = {-897, -890, -819, -803, -612, -480, -330, -151, 43, 334, 463, 625, 894, 917, 947};
		int array4[] = {-792, -706, -506, -464, -307, -285, -251, -236, -177, 37, 159, 359, 513, 731, 747};
		int array5[] = {-936, -895, -889, -813, -770, -602, -497, -366, -181, -133, -78, 177, 290, 429, 550, 558, 566, 616};
		int array6[] = {-932, -832, -696, -613, -470, -271, -138, -103, 54, 291, 405, 584, 796, 856, 901, 939, 948, 961, 997};

		System.out.printf("Array of data for N = 3: ");
		Array.printarray(array1);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array1, 3));
		System.out.println();

		System.out.printf("Array of data for N = 4: ");
		Array.printarray(array1);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array1, 4));
		System.out.println();

		System.out.printf("Array of data for N = 10: ");
		Array.printarray(array2);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array2, 10));
		System.out.println();

		System.out.printf("Array of data for N = 11: ");
		Array.printarray(array3);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array3, 11));
		System.out.println();

		System.out.printf("Array of data for N = 8: ");
		Array.printarray(array4);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array4, 8));
		System.out.println();

		System.out.printf("Array of data for N = 11: ");
		Array.printarray(array5);
		System.out.printf("Solution: ");
		Array.printarray(optimalSubsample(array5, 11));
		System.out.println();

		System.out.printf("Array of data for N = 13: ");
		Array.printarray(array6);
		Array.printarray(optimalSubsample(array6, 13));
		System.out.println();
		
	}
	
}

