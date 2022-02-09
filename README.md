## Prediction Confidence Planner

### Project description:
The application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from:
- holdout
    - Z-test -> use when holdout sample size is big (>30) and the distribution of the test statistic can be approximated by a normal distribution
    - T-test -> use when holdout sample size is small (<30) and the test statistic follows a normal distribution
    - Loose test set bound -> use when you would like to be sure that the obtained interval will be at least of provided confidence, the interval may be much wider than the tighest possible one
    - Clopper-Pearson -> use when you would like to be sure that the obtained interval will be at least of provided confidence, so the interval may be wider but not as wide as in the Loose test set bound
    - Wilson score -> use to obtain the interval, which on average is precisely for the given confidence; do not use when your accuracy is close to 0 or 1
- for bootstrap
    - Percentile Bootstrap Method -> use when number of bootstrap resamples is big (at least 100) and you have accuracies from each resample
- for Cross-Validation
    - cv_interval -> use when you have an accuracy from CV and you know number of samples and number of folds
- for Progressive Validation
    - prog_val -> use when you have an accuracy from Progressive Validation technique and you know test set size
    
Moreover, for z-test, t-test and loose test set bound there are reverse tests. With their help, when you know what confidence interval you want to obtain at a given confidence, tests will return number of samples needed for a holdout method.<br>
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence.<br>

### Folder structure description:
TODO

