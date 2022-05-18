# Long texts from website stored here for more readability

home_text = '''### **How to use the app**
The application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

#### **Map of usage**
'''
home_text_2 = '''
 - **Holdout methods** - Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.
 - **Bootstrap method** - Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.
 - **Cross-Validation method** - Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.
 - **Progressive Validation method** - Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams.
 
 - **Holdout methods**
    - **Z-test** - use when holdout sample size is big (>30) and the distribution of the test statistic can be approximated by a normal distribution
    - **T-test** - use when holdout sample size is small (<30) and the test statistic follows a normal distribution
    - **Loose test set bound** - use when you would like to be sure that the obtained interval will be at least of provided confidence, the interval may be much wider than the tighest possible one
    - **Clopper-Pearson** - use when you would like to be sure that the obtained interval will be at least of provided confidence, so the interval may be wider but not as wide as in the Loose test set bound
    - **Wilson score** - use to obtain the interval, which on average is precisely for the given confidence; do not use when your accuracy is close to 0 or 1
 - **Bootstrap method**
   - **Percentile Bootstrap** - use when number of bootstrap resamples is big (at least 100) and you have accuracies from each resample
 - **Cross-Validation method**
   - **Cross Validation** - use when you have an accuracy from CV and you know number of samples and number of folds
 - **Progressive Validation method**
   - **Progressive Validation** - use when you have an accuracy from Progressive Validation technique and you know test set size
    
Moreover, for z-test, t-test and loose test set bound there are reverse tests. With their help, when you know what confidence interval you want to obtain at a given confidence, tests will return number of samples needed for a holdout method.
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence.'''

about_text = '''
The **Prediction Confidence Planner** application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

### Contributors
 - Antoni Klorek, Poznan University of Technology
 - Karol Roszak, Poznan University of Technology
 - Dariusz Brzezinski, Poznan University of Technology

### References

1. Blum, A., Kalai, A., Langford, J.: Beating the hold-out: Bounds for k-fold and progressive cross-validation. In: Ben-David, S., Long, P.M. (eds.) Proceedings of the Twelfth Annual Conference on Computational Learning Theory, COLT 1999, Santa Cruz, CA, USA, July 7-9, 1999. pp. 203–208 (1999), [link](https://www.ri.cmu.edu/pub_files/pub1/blum_a_1999_1/blum_a_1999_1.pdf).
2. Clopper, C.J., Pearson, E.S.: The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4), 404–413 (1934), [link](http://www.jstor.org/stable/2331986).
3. Langford, J.: Tutorial on practical prediction theory for classification. J. Mach. Learn. Res. 6, 273–306 (2005), [link](https://www.jmlr.org/papers/volume6/langford05a/langford05a.pdf).
4. Puth, M.T., Neuhauser, M., Ruxton, G.: On the variety of methods for calculating confidence intervals by bootstrapping. The Journal of animal ecology 84 (06 2015), [link](https://doi.org/10.1111/1365-2656.12382).
5. Wilson, E.B.: Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association 22(158), 209–212 (1927), [link](http://www.jstor.org/stable/2276774).
'''

z_test_text = '''This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples, obtained accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

z_test_text_reverse_samples = '''Function takes difference from accuracy to lower/upper bound and confidence.
    Returns rounded number of samples which should be taken to obtain a given confidence interval.'''

z_test_text_reverse_confidence = '''Function takes difference from accuracy to lower/upper bound and number of samples.
    Returns confidence rounded to two decimal places.'''

t_test_text = '''This test works for smaller number of samples (<30), uses t-distribution.
    Function takes number of samples, obtained accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

t_test_text_reverse = '''Function takes difference from accuracy to lower/upper bound and number of samples.
    Returns confidence rounded to two decimal places.'''

loose_langford_text = '''Function takes number of samples, obtained accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

loose_langford_text_reverse_samples = '''Function takes difference from accuracy to lower/upper bound and confidence.
    Returns rounded number of samples which should be taken to obtain a given confidence interval.'''

loose_langford_text_reverse_confidence = '''Function takes difference from accuracy to lower/upper bound and number of samples.
    Returns confidence rounded to two decimal places.'''

clopper_pearson_text = '''Function takes number of samples, obtained accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

wilson_text = '''The Wilson method can be used to estimate confidence intervals of accuracy obtained on a holdout test 
set. Experiment with the controls below to get the interval for the specified confidence level, as well as 
the 90%, 95%, and 99% confidence intervals.'''

bootstrap_text = '''Function takes list of resamples accuracies obtained from bootstrap method (In comma separated format as shown) and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

cross_validation_text = '''Function takes number of samples, number of folds, obtained accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''

progressive_validation_text = '''Function takes number of samples from a test set, obtained from it accuracy and confidence.
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.'''