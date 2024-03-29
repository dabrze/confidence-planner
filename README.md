# confidence-planner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/dabrze/confidence-planner/actions/workflows/Tests.yml/badge.svg?branch=main)](https://github.com/dabrze/confidence-planner/actions/workflows/Tests.yml)
[![last commit](https://img.shields.io/github/last-commit/dabrze/confidence-planner)](https://github.com/dabrze/confidence-planner/commits/)
[![Discuss](https://img.shields.io/github/discussions/dabrze/confidence-planner)](https://github.com/dabrze/confidence-planner/discussions)

The **confidence-planner** package provides implementations of estimation procedures for confidence intervals 
around classification accuracy in Python. The package currently features approximations for holdout, bootstrap,
cross-validation, and progressive validation experiments. For information on how to install and use the package, 
read on or take a look at our demonstration video below. For a web application using the estimation methods, go to the `dash` branch of this repository.


https://user-images.githubusercontent.com/11019531/169568537-eb7e978b-7fbb-4d3f-a582-b8e4abca1a45.mp4


## Installing confidence-planner

To install confidence-planner, just execute:

```bash
pip install confidence-planner
```

Afterwards you can import `confidence_planner` and use all its functions.

## Quickstart

```python
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import confidence_planner as cp

# example dataset
X, y = datasets.load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=23
)

# training the classifier and calculating accuracy
clf = svm.SVC(gamma=0.001)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
acc = metrics.accuracy_score(y_test, y_pred)

# confidence interval and sample size estimation
ci = cp.estimate_confidence_interval(y_test.shape[0], acc, confidence_level=0.90)
sample = cp.estimate_sample_size(interval_radius=0.05, confidence_level=0.90)
print(f"90% CI: {ci}")
print(f"Samples needed for a 0.05 radius 90% CI: {sample}")
```

More code examples (including cross-validation and bootstrapping) can be found in the `examples` folder.

## Methods

**Holdout methods** Confidence and sample size estimations for accuracy on holdout test sets can be done with multiple methods.
The simplest method is to assume a normal distribution of the classifiers accuracy and then use the Z-test or t-test \[1\]. However,
there exist good approximations directly for binomial (0-1 loss) distribution. The Wilson method \[5\] offers the tightest confidence bounds
but might be slightly less reliable when accuracy is very close to 0.0 or 1.0. The Clopper-Pearson approximation \[4\] is more conservative, and the
Langford approximation \[1\] (based on the Hoeffding inequality) is the most conservative. For sample size and confidence level 
estimation, only the Langford and normal-distribution approximations are available.

**Cross-Validation method** Estimations for k-fold cross-validation experiments can be done using Blum's method \[2\]. This
 approximation is based on the Hoeffding inequality and is very conservative. It boils down to the fact that the confidence
 of k-fold experiment is no worse than a 1/k holdout experiment. Therefore, increasing the number of folds will make the
 confidence intervals wider.
 
**Bootstrap method** To estimate the confidence interval or confidence level of a bootstrapping experiment one can calculate
the percentiles of accuracies from all the bootstraps \[3\]. The larger the number of bootstraps, the more reliable the estimation will be. 
To estimate the sample size, one can assume a normal distribution of the bootstrap results and use the Z-test method.

**Progressive validation** Progressive validation is also known as time series validation, rolling validation, or the 
test-then-train method. In case of progressive validation experiments, one can use Langford's approximation and 
provide the size of the entire (rolled) dataset as the sample size \[2\].

Below a summary of the methods that can be used for different estimation tasks.

![Map of estimation methods](examples/img/map.svg)

## References

Confidence-planner methods belong to the field of frequentist statistics.

1. Langford J. (2005) Tutorial on practical prediction theory for classification. *Journal of Machine Learning Research* 6, 273–306, [link](https://www.jmlr.org/papers/volume6/langford05a/langford05a.pdf).
2. Blum A., Kalai, A., Langford, J. (1999) Beating the hold-out: Bounds for k-fold and progressive cross-validation. *Proceedings of the Twelfth Annual Conference on Computational Learning Theory, COLT 1999*, pp. 203–208, [link](https://www.ri.cmu.edu/pub_files/pub1/blum_a_1999_1/blum_a_1999_1.pdf).
3. Puth M.T., Neuhauser M., Ruxton G.(2015) On the variety of methods for calculating confidence intervals by bootstrapping. *The Journal of Animal Ecology* 84, [link](https://doi.org/10.1111/1365-2656.12382).
4. Clopper C.J., Pearson E.S. (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413, [link](http://www.jstor.org/stable/2331986).
5. Wilson E.B. (1927) Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158), 209–212, [link](http://www.jstor.org/stable/2276774).

## License 

Confidence-planner is free and open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Citing

If you use confidence-planner as part of your workflow in a scientific publication, please consider citing the associated [paper](https://arxiv.org/abs/2301.05702):

```
@article{confidence_planner,
  author       = {Antoni Klorek and Karol Roszak and Izabela Szczech and Dariusz Brzezinski},
  title        = {confidence-planner: Easy-to-Use Prediction Confidence Estimation and Sample Size Planning},
  year         = {2023},
  eprint       = {arXiv:2301.05702},
  doi          = {10.48550/arXiv.2301.05702}
}
```

- [Klorek, A. *et al.* (2023) confidence-planner: Easy-to-Use Prediction Confidence Estimation and Sample Size Planning. DOI: 10.48550/arXiv.2301.05702.](https://arxiv.org/abs/2301.05702)

## Contact

The best way to ask questions is via the [GitHub Discussions channel](https://github.com/dabrze/confidence-planner/discussions). 
In case you encounter usage bugs, please don't hesitate to use the [GitHub's issue tracker](https://github.com/dabrze/confidence-planner/issues) directly. 
