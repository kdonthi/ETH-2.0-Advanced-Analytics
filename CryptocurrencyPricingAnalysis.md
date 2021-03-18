# **Cryptocurrency Pricing Analysis**

## **Table of Contents**
 * [Introduction](#introduction)
 * [How to Run the Program](#how-to-run-the-program)
 * [Explanation](#explanation)

### **Introduction**
This program tries to predict blockchain pricing data using past blockchain pricing data using three steps:
<ol>
<li>Creating a polynomial regression of the training data.</li>
<li>Finding the local minima and maxima of the polynomial regression function</li>
<li>Creating new datasets where the data between local minima and maxima are replaced with the most evenly spaced numbers in the range</li>
<li>Running polynomial regression again on the “reduced” training data (you choose fraction to reduce data by)</li>
</ol>

### **How to Run the Program**
This program requires that it is at the same level as the EvenlySpacedNumbers directory, which is the way it is set already. Additionally, the only step needed is to use ```python3 CryptocurrencyPricingAnalysis.py __amount_to_reduce_data_in_reduced_model__``` to run it. For example, if we only wanted 80% of the initial data in the reduced model, we would do ```python3 CryptocurrencyPricingAnalysis.py 0.2```. I have found that the limits for the data reduction are best when 0.2 <= x <= 0.95

Upon running it, you will see a “Full Data Training cost” and a “Full Data Testing cost” - these are calculated by finding the mean square error of the model predicted by using <b>all</b> the data with around 11 features (from epoch to epoch^11 including log(epoch)). I normalized the epoch number and avg. pricing values so that (0,0) is set to the avg. price value around 5000 since values before that looked like outliers. The training data is the epoch and avg. pricing data from 5000 to 17000 epochs, inclusive, and the testing data is the epoch and avg. pricing data greater from epochs greater than 17000. I have also included features that capture the distance in days from Saturday, which I have seen as a day that blockchain stocks increase.

In addition, you will see a check to make sure that the amount of values in the matrix of x-values and day values is the same as the values in the y-values matrix for reduced values.

At this point, you should see a graph of the orignal values ("Actual"), a model by polynomial regression on all the data ("Full Data"), and a model by polynomial regression on the reduced data ("Reduced by x"). The vertical lines are local minima or maxima on the "Predicted" model. <br> <t>

<img width="617" alt="Screen Shot 2021-03-17 at 5 16 06 PM" src="https://user-images.githubusercontent.com/8030450/111554900-76777c00-8744-11eb-93da-79e6493058d0.png">

### **Explanation**
You may be wondering why I fit two models on the same data. The reason for this is that blockchain data is usually VERY noisy. 

![Screen Shot 2021-03-16 at 7 12 59 PM](https://user-images.githubusercontent.com/8030450/111404227-a282f680-868b-11eb-8223-21616eaabc70.png)


You can see the local minima and maxima for this data are out of control.

I realized that I could reduce the amount of noise by reducing the actual amount of data present. But it wouldn’t have made sense to just remove data randomly, so I used a randomized algorithm called *OptimalSubsampleNew.py* in my “EvenlySpacedNumbers” folder to select evenly spaced numbers in each decreasing or increasing interval found in the 11 degree polynomial regression model and created a new dataset with the evenly spaced values spaced out at regular intervals. If you want to read more about my randomized algorithm, you can go to the README.md in my "EvenlySpacedNumbers” folder. 

Three methods I used in my machine learning model were:

<ol>
  <li> Shifting the data set so that it started at epoch 5000 and setting the epoch and avg price values such that the lowest epoch was 1 and y value was around 0 (the reason x is 1 is that I found that using log(x) was a really useful feature to decrease both training and testing error and you cannot take log(0)). </li>
  <li> Min-max normalization of the features - After finding the column of each features, I set each value to ```x_i - column.min / column.max - column.min``` to make sure that all the values for all of the features were in the same range of [0,1]. </li>
  <li> Solving for the weight matrix directly without using gradient descent. Since I have only around 14 features, I decided to solve for the weight matrix that minimizes the cost function directly. dC/dW = xT*(xW - y) (and we set dC/dW to 0) ==> xTy = xTxW ==> (xTx)^-1xTy = W. Make sure you DO NOT include two of the same features when creating your feature matrix because this will cause the matrix to be singular/non-invertible.</li>
</ol>

If you are wondering why I didn't use a neural network instead, I did. It resulted in a more straight line of fit than my polynomial regression model when I created a 3 layer model. I have included the code in my file in a function called ```neuralNetwork``` to which you just pass in a X matrix containing all the features (X), the output vector (y), the number of units in your hidden layer (N), and the learning rate (alpha). I have found that alpha really only cooperates when it is set to 0.0001. If you don't really want to do any of this manually, I have included a variable called ```nnwpred``` which you can uncomment on line 173. You can replace ```pred``` with ```nnwpred``` on the next line to see the prediction and run ```plt.show()``` on the line after to see the prediction.

<img width="629" alt="Screen Shot 2021-03-17 at 5 25 44 PM" src="https://user-images.githubusercontent.com/8030450/111555521-cf93df80-8745-11eb-95e4-25640c9c5c75.png">

