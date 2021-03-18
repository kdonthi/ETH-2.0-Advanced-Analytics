# **ETH 2.0 Stock Prediction**

## **Overview**
<p> This is a project to create advanced analytics about the blockchain. I have created a program to create a histogram to measure a specific validator's performance against other validators (```Histogram.py``` with instructions in ```Histogram.md```) and a program to develop a model to predict Blockchain prices (```CryptocurrencyPricingAnalysis.py``` with instructions in ```CryptocurrencyPricingAnalysis.md```). <p>

## **To Do**
Right now, my accuracy rate on the test set is not too great, even with my reduced data algorithm.

Some possible next steps are listed below include:
<ol>
<li> I have a Java program in my ```EvenlySpacedNumbers``` directory called ```optimalSubsample.java```. This is a much more accurate and fast algorithm than my randomized one, but the only caveat is that you should transform the code from Java to Python. </li>
<li> Find features to create a better fitting neural network/polynomial regression model. For some reason, I cannot get a model to overfit the data to capture the local minima and maxima. I have include features for "distance from Saturday" and normalized "epoch Number", so you can either do new combinations of these or find new ones altogether.
<ol>
