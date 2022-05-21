palette = ["#cc6677", "#f6cf71", "#0f8554", "#1d6996", "#ff9900"]

marks_accuracy = {
    0: {"label": "0.0", "style": {"color": "black"}},
    0.1: {"label": "0.1", "style": {"color": "black"}},
    0.2: {"label": "0.2", "style": {"color": "black"}},
    0.3: {"label": "0.3", "style": {"color": "black"}},
    0.4: {"label": "0.4", "style": {"color": "black"}},
    0.5: {"label": "0.5", "style": {"color": "black"}},
    0.6: {"label": "0.6", "style": {"color": "black"}},
    0.7: {"label": "0.7", "style": {"color": "black"}},
    0.8: {"label": "0.8", "style": {"color": "black"}},
    0.9: {"label": "0.9", "style": {"color": "black"}},
    1.0: {"label": "1.0", "style": {"color": "black"}},
}

marks_interval = {
    0: {"label": "0.0", "style": {"color": "black"}},
    0.1: {"label": "0.1", "style": {"color": "black"}},
    0.2: {"label": "0.2", "style": {"color": "black"}},
    0.3: {"label": "0.3", "style": {"color": "black"}},
    0.4: {"label": "0.4", "style": {"color": "black"}},
    0.5: {"label": "0.5", "style": {"color": "black"}},
}

marks_confidence = {
    0: {"label": "0%", "style": {"color": "black"}},
    0.1: {"label": "10%", "style": {"color": "black"}},
    0.2: {"label": "20%", "style": {"color": "black"}},
    0.3: {"label": "30%", "style": {"color": "black"}},
    0.4: {"label": "40%", "style": {"color": "black"}},
    0.5: {"label": "50%", "style": {"color": "black"}},
    0.6: {"label": "60%", "style": {"color": "black"}},
    0.7: {"label": "70%", "style": {"color": "black"}},
    0.8: {"label": "80%", "style": {"color": "black"}},
    0.9: {"label": "90%", "style": {"color": "black"}},
    1: {"label": "100%", "style": {"color": "black"}},
}

descriptions_dict = {
    "ci_holdout_wilson": """
    The Wilson method offers the tightest bounds for holdout confidence interval estimation. However, the method might 
    be slightly less reliable when accuracy is very close to 0.0 or 1.0. In such cases, one may want to compare the 
    estimate with the results of the Clopper-Pearson method. Use the controls below to experiment with different 
    settings. The method will return intervals for the specified confidence level, as well as 90%, 95%, and 99% 
    confidence intervals.""",

    "ci_holdout_clopper_pearson": """
    The Clopper-Pearson method is the more conservative alternative to the Wilson method for estimating confidence
    intervals of holdout test results. Use the controls below to experiment with different 
    settings. The method will return intervals for the specified confidence level, as well as 90%, 95%, and 99% 
    confidence intervals.""",

    "ci_holdout_langford": """
    The Langford method is a very conservative estimation based on the Hoeffding inequality. Along with the Wilson
    and Clopper-Pearson method it is suitable for accuracy estimates without any additional assumptions.
    Use the controls below to experiment with different settings. The method will return intervals for 
    the specified confidence level, as well as 90%, 95%, and 99% confidence intervals.""",

    "ci_holdout_z_test": """
    This estimation procedure assumes the accuracies of the classifier are normally distributed around the mean. 
    This is a simplified estimate, but easy to use in many situations. The 
    estimates might be overly optimistic if the sample size is small or the classifier is not stable.
    Use the controls below to experiment with different settings. The method will return intervals for 
    the specified confidence level, as well as 90%, 95%, and 99% confidence intervals.""",

    "ci_holdout_t_test": """
    This estimation procedure assumes the accuracies of the classifier are normally distributed around the mean 
    on a small (< 30) sample size. This is a simplified estimate, but easy to use in many situations. The 
    estimates might be overly optimistic if the sample size is small or the classifier is not stable. 
    Use the controls below to experiment with different settings. The method will return intervals for 
    the specified confidence level, as well as 90%, 95%, and 99% confidence intervals.""",

    "ci_progressive": """
    Progressive validation (also known as time series validation, rolling cross-validation, or
    as the test-then-train method) starts off with a small subset of data for training purposes, predicts for the 
    later data points in the dataset and then checks the accuracy for the predicted data points. In this procedure, as 
    the sample size, provide the total of examples that were used for testing (this can be practically the entire 
    dataset). Use the controls below to experiment with different settings. The method will return intervals for 
    the specified confidence level, as well as 90%, 95%, and 99% confidence intervals.""",
    
    "ci_cv": """
    Estimations for k-fold cross-validation are based on the Hoeffding inequality and are very conservative. 
    The confidence of k-fold experiment is only no worse than a 1/k holdout experiment. Therefore, increasing the 
    number of folds will make the confidence intervals wider. Use the controls below to experiment with different 
    settings. The method will return intervals for the specified confidence level, as well as 90%, 95%, and 99% 
    confidence intervals.""",

    "ci_bootstrap": """
    The confidence interval of a bootstrapping experiment is calculated based on the percentiles 
    of accuracies from all the bootstraps. The larger the number of bootstraps, the more reliable the estimation.
    Use the controls below to experiment with different settings. The method will return intervals for 
    the specified confidence level, as well as 90%, 95%, and 99% confidence intervals.""",

    "sample_size_holdout_langford": """
    Conservative sample size estimation based on the Hoeffding inequality. 
    Use the controls below to experiment with different settings.""",

    "sample_size_holdout_z_test": """
    This estimation procedure assumes the accuracies of the classifier are normally
    distributed around the mean. This is a simplified estimate, but is much less conservative than the Langford
    method. Use the controls below to experiment with different settings.""",
    
    "sample_size_progressive": """
    Progressive validation (also known as time series validation, rolling cross-validation, or
    as the test-then-train method) starts off with a small subset of data for training purposes, predicts for the 
    later data points in the dataset and then checks the accuracy for the predicted data points. Use the controls 
    below to experiment with different settings.""",

    "sample_size_cv": """
    Estimations for k-fold cross-validation are based on the Hoeffding inequality and are very conservative. 
    The confidence of k-fold experiment is only no worse than a 1/k holdout experiment. Therefore, increasing the 
    number of folds will make the required sample sizes larger. Use the controls below to experiment with different 
    settings.""",

    "sample_size_bootstrap": """
    The confidence intervals of a bootstrapping experiments are calculated based on the percentiles 
    of accuracies from all the bootstraps. Therefore, assuming a large number of bootstraps one can estimate the 
    sample size by assuming a normal distribution and using the Z-test statistic. Use the controls below to 
    experiment with different settings.""",
    
    "confidence_level_holdout_langford": """
    Conservative confidence level estimation based on the Hoeffding inequality. 
    Use the controls below to experiment with different settings.""",

    "confidence_level_holdout_z_test": """
    This estimation procedure assumes the accuracies of the classifier are normally
    distributed around the mean. This is a simplified estimate, but is much less conservative than the Langford
    method. Use the controls below to experiment with different settings.""",

    "confidence_level_holdout_t_test": """
    This estimation procedure assumes the accuracies of the classifier are normally
    distributed around the mean. This is a simplified estimate, but is much less conservative than the Langford
    method. Use the controls below to experiment with different settings.""",

    "confidence_level_progressive": """
    Progressive validation (also known as time series validation, rolling cross-validation, or
    as the test-then-train method) starts off with a small subset of data for training purposes, predicts for the 
    later data points in the dataset and then checks the accuracy for the predicted data points. Use the controls 
    below to experiment with different settings.""",

    "confidence_level_cv": """
    Estimations for k-fold cross-validation are based on the Hoeffding inequality and are very conservative. 
    The confidence of k-fold experiment is only no worse than a 1/k holdout experiment. Therefore, increasing the 
    number of folds will make the confidence levels smaller. Use the controls below to experiment with different 
    settings.""",

    "confidence_level_bootstrap": """
    The confidence level of an interval for bootstrapping experiment is calculated based on the percentiles 
    of accuracies from all the bootstraps. The larger the number of bootstraps, the more reliable the estimation.
    Use the controls below to experiment with different settings.""",

    "about": """
The Confidence Planner website is a companion website to conifdence-planner python package that can be found on PyPI and
 Github: https://github.com/dabrze/confidence-planner. The package will allow you to integrate confidence interval
 estimations into your sklearn-based or any other machine learning analyses. If you have any questions or comments 
 please let us know in the project's [github discussion page](https://github.com/dabrze/confidence-planner/discussions).

### Contributors
 - Antoni Klorek, Poznan University of Technology
 - Karol Roszak, Poznan University of Technology
 - Dariusz Brzezinski, Poznan University of Technology""",
    "methods": """
**Holdout methods** Confidence and sample size estimations for accuracy on holdout test sets can be done with 
multiple methods. The simplest method is to assume a normal distribution of the classifiers accuracy and then use the 
Z-test or t-test \[1\]. However, there exist good approximations directly for binomial (0-1 loss) distribution. The 
Wilson method \[5\] offers the tightest confidence bounds but might be slightly less reliable when accuracy is very 
close to 0.0 or 1.0. The Clopper-Pearson approximation \[4\] is more conservative, and the Langford 
approximation \[1\] (based on the Hoeffding inequality) is the most conservative. For sample size and confidence level 
estimation, only the Langford and normal-distribution approximations are available.

**Cross-Validation method** Estimations for k-fold cross-validation experiments can be done using Blum's method \[2\]. 
This approximation is based on the Hoeffding inequality and is very conservative. It boils down to the fact that the 
confidence of k-fold experiment is no worse than a 1/k holdout experiment. Therefore, increasing the number of folds 
will make the confidence intervals wider.

**Bootstrap method** To estimate the confidence interval or confidence level of a bootstrapping experiment one can 
calculate the percentiles of accuracies from all the bootstraps \[3\]. The larger the number of bootstraps, the more 
reliable the estimation will be. To estimate the sample size, one can assume a normal distribution of the bootstrap 
results and use the Z-test method.

**Progressive validation** Progressive validation is also known as time series validation, rolling validation, or the 
test-then-train method. In case of progressive validation experiments, one can use Langford's approximation and 
provide the size of the entire (rolled) dataset as the sample size \[2\].""",

    "references": """
1. Langford J. (2005) Tutorial on practical prediction theory for classification. *Journal of Machine Learning Research* 6, 273–306, [link](https://www.jmlr.org/papers/volume6/langford05a/langford05a.pdf).
2. Blum A., Kalai, A., Langford, J. (1999) Beating the hold-out: Bounds for k-fold and progressive cross-validation. *Proceedings of the Twelfth Annual Conference on Computational Learning Theory, COLT 1999*, pp. 203–208, [link](https://www.ri.cmu.edu/pub_files/pub1/blum_a_1999_1/blum_a_1999_1.pdf).
3. Puth M.T., Neuhauser M., Ruxton G.(2015) On the variety of methods for calculating confidence intervals by bootstrapping. *The Journal of Animal Ecology* 84, [link](https://doi.org/10.1111/1365-2656.12382).
4. Clopper C.J., Pearson E.S. (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413, [link](http://www.jstor.org/stable/2331986).
5. Wilson E.B. (1927) Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158), 209–212, [link](http://www.jstor.org/stable/2276774).
""",
}
