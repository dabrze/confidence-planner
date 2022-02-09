# Long texts from website stored here for more readability

home_text = '''### **How to use the app**
The application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

#### **Map of usage**
'''
home_text_2 = '''#### **More insightfull about options and methods**
- **Holdout methods** -> Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.
    - **Z-test** -> use when holdout sample size is big (>30) and the distribution of the test statistic can be approximated by a normal distribution
    - **T-test** -> use when holdout sample size is small (<30) and the test statistic follows a normal distribution
    - **Loose test set bound** -> use when you would like to be sure that the obtained interval will be at least of provided confidence, the interval may be much wider than the tighest possible one
    - **Clopper-Pearson** -> use when you would like to be sure that the obtained interval will be at least of provided confidence, so the interval may be wider but not as wide as in the Loose test set bound
    - **Wilson score** -> use to obtain the interval, which on average is precisely for the given confidence; do not use when your accuracy is close to 0 or 1
- **Bootstrap method** -> Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.
    - **Percentile Bootstrap Method** -> use when number of bootstrap resamples is big (at least 100) and you have accuracies from each resample
- **Cross-Validation method** -> Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.
    - **Cross Validation Method** -> use when you have an accuracy from CV and you know number of samples and number of folds
- **Progressive Validation method** -> Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams.
    - **Progressive Validation Method** -> use when you have an accuracy from Progressive Validation technique and you know test set size
    
Moreover, for z-test, t-test and loose test set bound there are reverse tests. With their help, when you know what confidence interval you want to obtain at a given confidence, tests will return number of samples needed for a holdout method.<br>
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence.<br>'''

about_text = '''### **About the project**
Abrakadabra TODO

### **Contributors**
 - Mario
 - Dario
 - ...
'''

z_test_text = '''This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''