<h1> Evenly-Spaced-Numbers </h1>

The goal of these programs is to find the N most evenly spaced numbers in a sorted set of numbers. The motivation was originally to declutter dark matter density data but I realized that it could be used for blockchain pricing data as well.

Testcases:
```[1,2,3,4,100]; N = 3 ==> [1,4,100]``` </br>
```[1,2,3,4,100]; N = 4 ==> [1,2,4,100]``` </br>
```[0,33,50,66,100]; N = 3 ==> [0,50,100]``` </br>
```[0,33,50,66,100]; N = 4 ==> [0,33,66,100]``` </br>

Cost Function for Evenness (code in Python3):

```
set = [x_1, x_2, x_3,...,x_n]
N = n
optimalDistance = (x_n - x_1) / (N - 1)
evennessCost = 0
for i,j in zip(set, set[1:]):
  evennessCost += ((j - i) - optimalDistance) ** 2 #basically sum of square errors between successive distances and optimalDistance
```
<h2> optimalSubsampleNew.py </h2>
This is a randomized algorithm finds an evenly spaced set in time complexity O(n^2). I do this by going through each number in a list, and shifting it right or left to minimize its MSE of its distances to its right or left with the "optimal distance", which is the (end - beginning) / (N - 1).

Like K-means, this can get stuck in local minima, so I use reinitializations to try to find the global minima. I have 100% accuracy on 20,000 samples, using a less efficient recursive tree method (```optimalSubsampleTrees.py```) going through possibilities of the list as "base truth".

Run ```python3 main.py``` with all the files in your directory to run the stress test, or run ```OptimalSubsampleNew.py``` and insert your own test case in the format:

like ```print(optimalSubsample(list(range(100)),10))```
or ```print(optimalSubsample([1,2,3,4,5],3)```.

Make sure the second parameter (an integer), "N", is <= to the length of your first parameter (a list) and >= 2 (because the first and last number of the list provided are always in the resulting list.)

<h2> optimalSubsample.java </h2>
I have created a dynamic programming solution in Java by storing the evennessCost of lists continuous to the end of the array.

You can run this solution by compiling using ```javac optimalSubsample.java``` and then ```java optimalSubsample```. You can adjust the arrays given and the numbers to choose for each array. <br/>

E.g. change the numbers in an array in the main class ```int array1[] = {0, 33, 50, 66, 100};``` and then run ```Array.printarray(optimalSubsample(array1, 4));``` (for N = 4). 
