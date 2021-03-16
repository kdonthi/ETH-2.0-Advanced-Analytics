<h1>Histogram Program Explanation</h1>

<h2> How to run the Program </h2>

The file ```histogram.py``` creates a histogram of the average inclusion distances of <i>n</i> randomly chosen validators and compares it to the average inclusion distance of a given validator index. 
To run the program, you can either install pandas, matlplotlib, and the requests libraries (with ```pip3 install libname```) or you can just start up the virtual environment I have set up called ```histogramenv``` using ```source histogramenv/bin/activate``` and run ```python3 histogram.py```.

```histogram.py``` requires two arguments to produce the histogram:
  <ol>
    <li> The number of validators you want the histogram to contain.
      
    <li> The index of the validator you want to compare i.e. ```0,1,2,3,...,87749```.
  </ol> </br>
  
  Therefore, running the file should look like this: ```python3 histogram.py 10 0``` (if you want to plot 10 validators and see how the validator with index 0 compares to them). </br>
  
  The first number can technically be from 0 <= n <= 87750, and the second number can be from 0 <= m <= 87749 but the Beaconcha.in API I used to get the data for the histogram is not perfect in getting the data for each value. Furthermore, the program takes around 4.3 seconds to create a histogram for 10 validators so even plotting 1000 validators can take around 6 minutes. Therefore, it is better to be conservative in the number of validators we choose to plot (around 100 to 2000 is good).  </br>
  
  The program will output the validator number we are trying to include (not to be mistaken for index, i.e. 3 means we are trying to get our 3rd validator) into the histogram, the average inclusion distance of the validator you are looking at, a histogram, and after you close the histogram, the percentile of the validator you passed in as the 2nd argument. The histogram contains the distribution of the randomly chosen IDs' inclusion distances, with the addition of the validator's average inclusion distance if it was not already chosen randomly, and a vertical line in the location of the specified validator's avg. inclusion distance. Once the histogram is closed, you will see what percentile that validator is in in the given data (assumed that is it better to have a smaller avg. inclusion distance.) </br>
  
  <b>NOTE:</b> Sometimes, you will see the same number repeating over and over again for the validator count. This means that the API is not collaborating with the program to give the data.  You can wait for the issue to fix itself, increase the number of tries you do for each call (I have included the number of tries for each API call as an optional third argument, which is set to 5 by default, e.g. ```python3 histogram.py 10 0 6``` does 6 tries instead of 5), or just try again at a later time.
  
<h2> Explanation of Program </h2> </br>

<p1> I decided to use inclusion distance as a measure of validator performance because validators' effectiveness is based on how active they are in a network. Each validator has the opportunity to say a block someone else created/"proposed" is correct, or "attest" to a block. 
  The network depends on these validators, or "attestors", to be active and act as a source of authority. Therefore, one measure of seeing how helpful an attestor is to see how quickly they respond to their task; a more active attestor will have less slots, or blocks of time between the "attestation slot", or when they were given the task to validate a block, and 
 the "inclusion slot", or when they actually performed the validation. For reference, each epoch is 6.4 minutes long and contains 32 slots, meaning that each slot is 0.2 minutes or 12 seconds long. </p1> </br> </br>
 
<p2> Furthermore, I decided to calculate the percentile of a given validator by taking the average of two different percentile methods:
  <ol> 
    <li>the average of the percent of total values the value is <b>less than</b> and 
    <li>the percent of total values the value is <b>less than or equal to</b>
  </ol> </br>
  To understand why I did this, let me propose a hypothetical scenario where we are trying to find the percentile of a "1" in a histogram of a 1000 1's. Does it make more sense to say our value is close to the 100th percentile or the 0th percentile? To me, it seems that both options are too extreme. If we have a group of the same values, the perentile of a value should be the average of the extremes, or 50th percentile in this example. <p2> </br>
  
tl;dr:
<ol>
  <li> Pull this directory, ```Stakey```.
  
  <li> Set up the virtual environment using ```source histogramenv/bin/activate```.
  
  <li> Run the file ```histogram.py ____number of random validators____ ____validator index____ (optional: ____amount of tries for each call____)```
  <ul>
    <li> 0 <= __number of random validators__ <= 87750
    <li> 0 <= __validator index__ <= 87749 (one less than number of random validators, because it is possible to have no random validators)
    <li> 1 <= __amount of tries for each call__ < infinity (default is set to 5)
  </ul>
</ol>
  
