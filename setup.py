import setuptools

with open("README.md", "r", encoding='UTF8') as fh:

    long_description = fh.read()

setuptools.setup(
    name="confidence-planner",
    version="0.0.2",
    author="Antoni Klorek, Karol Roszak",
    author_email="antoni.klorek@student.put.poznan.pl",
    description="Python package for calculating confidence interval for model's accuracy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dabrze/confidence-planner",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.1",
        "statsmodels>=0.12.1"
    ]
)
