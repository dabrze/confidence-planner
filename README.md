[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Tests](https://github.com/Lorakszak/prediction-confidence-planner/actions/workflows/Tests.yml/badge.svg)
<!-- ![Package upload](https://github.com/Lorakszak/prediction-confidence-planner/actions/workflows/python-publish.yml/badge.svg) -->
![Repo size](https://img.shields.io/github/repo-size/Lorakszak/prediction-confidence-planner)
![Last commit](https://img.shields.io/github/last-commit/Lorakszak/prediction-confidence-planner)
![Discussions](https://img.shields.io/github/discussions/Lorakszak/prediction-confidence-planner)

 <!-- ![GitHub contributors](https://img.shields.io/github/contributors/Lorakszak/prediction-confidence-planner) # contributors (opt)-->
<!--  [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) #python version (only 1)-->
<!-- ![pypi](https://img.shields.io/pypi/v/pybadges.svg) -->
<!-- ![versions](https://img.shields.io/pypi/pyversions/pybadges.svg) -->

## Prediction Confidence Planner

### Project description:
The application provides different methods for calculating confidence interval for obtained accuracy from different training/testing techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from:
- **Holdout methods** - Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.
 - **Bootstrap method** - Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.
 - **Cross-Validation method** - Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.
 - **Progressive Validation method** - Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams.

 - **Holdout methods:**
   - **Z-test** - use when holdout sample size is big (>30) and the distribution of the test statistic can be approximated by a normal distribution
   - **T-test** - use when holdout sample size is small (<30) and the test statistic follows a normal distribution
   - **Loose test set bound** - use when you would like to be sure that the obtained interval will be at least of provided confidence, the interval may be much wider than the tighest possible one
   - **Clopper-Pearson** - use when you would like to be sure that the obtained interval will be at least of provided confidence, so the interval may be wider but not as wide as in the Loose test set bound
   - **Wilson score** - use to obtain the interval, which on average is precisely for the given confidence; do not use when your accuracy is close to 0 or 1
 - **Bootstrap method:**
   - **Percentile Bootstrap** - use when number of bootstrap resamples is big (at least 100) and you have accuracies from each resample
 - **Cross-Validation method:**
   - **Cross Validation** - use when you have an accuracy from CV and you know number of samples and number of folds
 - **Progressive Validation method:**
   - **Progressive Validation** - use when you have an accuracy from Progressive Validation technique and you know test set size
    
Moreover, for z-test, t-test and loose test set bound there are reverse tests. With their help, when you know what confidence interval you want to obtain at a given confidence, tests will return number of samples needed for a holdout method.
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence.

### Installation
Just type in
```bash
pip install confidence-planner
```

### Example usage for holdout
```python
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
from confidence_planner import confidence_planner

digits = datasets.load_digits()

# Flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
clf = svm.SVC(gamma=0.001)

# Split data into 70% train and 30% test subsets
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target, test_size=0.3, shuffle=False
)

# Learn the digits on the train subset
clf.fit(X_train, y_train)

# Predict the value of the digit on the test subset
predicted = clf.predict(X_test)

# Get the model's accuracy in the form of percentages
accuracy_percents = 100*metrics.accuracy_score(y_test, predicted)

# Print confidence interval around the obtained accuracy with 85% confidence
print(confidence_planner.wilson(len(y_test), accuracy_percents, 0.85))
```


### Example usage for bootstrap
```python
from sklearn import datasets, svm, metrics
from sklearn.utils import resample
from confidence_planner import confidence_planner

digits = datasets.load_digits()

# Flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
clf = svm.SVC(gamma=0.001)

n_iter = 100
accuracies = []

# Run model training and testing n_iter times
for i in range(n_iter):
    # Bootstrap indices
    indices = resample(range(n_samples), n_samples=n_samples)

    X_train = []
    y_train = []
    X_test = []
    y_test = []

    # Append images and labels with bootstrapped indices to lists for training
    for idx in indices:
        X_train.append(data[idx])
        y_train.append(digits.target[idx])

    # Append images and labels that are not in a training subset to lists for testing
    for i in range(n_samples):
        if i not in indices:
            X_test.append(data[i])
            y_test.append(digits.target[i])

    # Learn the digits on the train subset
    clf.fit(X_train, y_train)

    # Predict the value of the digit on the test subset
    predicted = clf.predict(X_test)

    # Get the model's accuracy in the form of percentages
    accuracy_percents = 100*metrics.accuracy_score(y_test, predicted)

    # Append accuracy to the list
    accuracies.append(accuracy_percents)

# Print confidence interval around the obtained accuracy with 85% confidence
print(confidence_planner.percentile_BM(accuracies, 0.85))
```


### Example usage for cross validation
```python
from numpy import mean
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import datasets, svm
from confidence_planner import confidence_planner

digits = datasets.load_digits()

# Flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
clf = svm.SVC(gamma=0.001)

# Prepare the cross-validation procedure
n_splits = 10
cv = KFold(n_splits=n_splits, shuffle=True)

# Evaluate model
scores = cross_val_score(clf, data, digits.target, scoring='accuracy', cv=cv, n_jobs=-1)

# Get the model's accuracy in the form of percentages
accuracy_percents = 100*mean(scores)

# Print confidence interval around the obtained accuracy with 85% confidence
print(confidence_planner.cv_interval(n_samples, n_splits, accuracy_percents, 0.85))
```


### Example usage for progressive validation
```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn import datasets, svm, metrics
from confidence_planner import confidence_planner

digits = datasets.load_digits()

# Flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
clf = svm.SVC(gamma=0.001)

# Create a time series split
n_splits = 10
n_test = len(digits.target)//(n_splits+1)
tscv = TimeSeriesSplit(n_splits=n_splits, test_size=n_test)

accuracies = []
# Perform training and testing on splits
for train_index, test_index in tscv.split(data):
    X_train, X_test = data[train_index], data[test_index]
    y_train, y_test = digits.target[train_index], digits.target[test_index]
    # Learn the digits on the train subset
    clf.fit(X_train, y_train)
    # Predict the value of the digit on the test subset
    predicted = clf.predict(X_test)
    # Get the model's accuracy in the form of percentages
    accuracy_percents = 100*metrics.accuracy_score(y_test, predicted)
    accuracies.append(accuracy_percents)

# Print confidence interval around the obtained accuracy with 85% confidence
print(confidence_planner.prog_val(n_test, np.mean(accuracies), 0.85))
```

For more examples see examples directory.
