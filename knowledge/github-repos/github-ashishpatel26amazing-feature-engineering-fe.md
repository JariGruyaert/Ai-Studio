---
title: "GitHub - ashishpatel26/Amazing-Feature-Engineering: Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself."
source: https://github.com/ashishpatel26/Amazing-Feature-Engineering
type: github-repo
extracted: 2026-01-18T12:45:28.767181
domain: github.com
word_count: 1194
processing_status: completed
---

# GitHub - ashishpatel26/Amazing-Feature-Engineering: Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself.

## Description
Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself. - ashishpatel26/Amazing-Feature-Engineering

## Content

ashishpatel26

/

Amazing-Feature-Engineering

Public

Notifications

You must be signed in to change notification settings

Fork

275

Star

764

Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself.

764

stars

275

forks

Branches

Tags

Activity

Star

Notifications

You must be signed in to change notification settings

ashishpatel26/Amazing-Feature-Engineering

master
Branches
Tags
Go to file
Code
Open more actions menu
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit

History
15 Commits
.github/
workflows
.github/
workflows

data
data

data_exploration
data_exploration

feature_cleaning
feature_cleaning

feature_engineering
feature_engineering

feature_selection
feature_selection

images
images

output
output

.gitignore
.gitignore

1_Demo_Data_Explore.ipynb
1_Demo_Data_Explore.ipynb

2.1_Demo_Missing_Data.ipynb
2.1_Demo_Missing_Data.ipynb

2.2_Demo_Outlier.ipynb
2.2_Demo_Outlier.ipynb

2.3_Demo_Rare_Values.ipynb
2.3_Demo_Rare_Values.ipynb

3.1_Demo_Feature_Scaling.ipynb
3.1_Demo_Feature_Scaling.ipynb

3.2_Demo_Discretisation.ipynb
3.2_Demo_Discretisation.ipynb

3.3_Demo_Feature_Encoding.ipynb
3.3_Demo_Feature_Encoding.ipynb

3.4_Demo_Feature_Transformation.ipynb
3.4_Demo_Feature_Transformation.ipynb

3.5_Demo_Feature_Generation.ipynb
3.5_Demo_Feature_Generation.ipynb

4.1_Demo_Feature_Selection_Filter.ipynb
4.1_Demo_Feature_Selection_Filter.ipynb

4.2_Demo_Feature_Selection_Wrapper.ipynb
4.2_Demo_Feature_Selection_Wrapper.ipynb

4.3_Demo_Feature_Selection_Embedded.ipynb
4.3_Demo_Feature_Selection_Embedded.ipynb

4.4_Demo_Feature_Selection_Feature_Shuffling.ipynb
4.4_Demo_Feature_Selection_Feature_Shuffling.ipynb

4.5_Demo_Feature_Selection_Hybrid_method.ipynb
4.5_Demo_Feature_Selection_Hybrid_method.ipynb

A Short Guide for Feature Engineering and Feature Selection.md
A Short Guide for Feature Engineering and Feature Selection.md

A Short Guide for Feature Engineering and Feature Selection.pdf
A Short Guide for Feature Engineering and Feature Selection.pdf

README.md
README.md

View all files
Repository files navigation
Feature Engineering & Feature Selection

A comprehensive guide
[pdf]

[markdown]
for
Feature Engineering
and
Feature Selection
, with implementations and examples in Python.

Motivation

Feature Engineering & Selection is the most essential part of building a useable machine learning project, even though hundreds of cutting-edge machine learning algorithms coming in these days like deep learning and transfer learning. Indeed, like what Prof Domingos, the author of  'The Master Algorithm' says:

“At the end of the day, some machine learning projects succeed and some fail. What makes the difference? Easily the most important factor is the features used.”

— Prof. Pedro Domingos

Data and feature has the most impact on a ML project and sets the limit of how well we can do, while models and algorithms are just approaching that limit. However, few materials could be found that systematically introduce the art of feature engineering, and even fewer could explain the rationale behind. This repo is my personal notes from learning ML and serves as a reference for Feature Engineering & Selection.

Download

Download the PDF here:

PDF Download

Same, but in markdown:

Mark Down Download

PDF has a much readable format, while Markdown has auto-generated anchor link to navigate from outer source. GitHub sucks at displaying markdown with complex grammar, so I would suggest read the PDF or download the repo and read markdown with
Typora
.

What You'll Learn

Not only a collection of hands-on functions, but also explanation on
Why
,
How
and
When
to adopt
Which
techniques of feature engineering in data mining.

the nature and risk of data problem we often encounter

explanation of the various feature engineering & selection techniques

rationale to use it

pros & cons of each method

code & example

Getting Started

This repo is mainly used as a reference for anyone who are doing feature engineering, and most of the modules are implemented through scikit-learn or its communities.

To run the demos or use the customized function,  please download the ZIP file from the repo or just copy-paste any part of the code you find helpful. They should all be very easy to understand.

Required Dependencies
:

Python 3.5, 3.6 or 3.7

numpy>=1.15

pandas>=0.23

scipy>=1.1.0

scikit_learn>=0.20.1

seaborn>=0.9.0

Table of Contents and Code Examples

Below is a list of methods currently implemented in the repo.

1. Data Exploration

1.1 Variables

1.2 Variable Identification

Check Data Types
[guide]

[demo]

1.3 Univariate Analysis

Descriptive Analysis
[guide]

[demo]

Discrete Variable Barplot
[guide]

[demo]

Discrete Variable Countplot
[guide]

[demo]

Discrete Variable Boxplot
[guide]

[demo]

Continuous Variable Distplot
[guide]

[demo]

1.4 Bi-variate Analysis

Scatter Plot
[guide]

[demo]

Correlation Plot
[guide]

[demo]

Heat Map
[guide]

[demo]

2. Feature Cleaning

2.1 Missing Values

Missing Value Check
[guide]

[demo]

Listwise Deletion
[guide]

[demo]

Mean/Median/Mode Imputation
[guide]

[demo]

End of distribution Imputation
[guide]

[demo]

Random Imputation
[guide]

[demo]

Arbitrary Value Imputation
[guide]

[demo]

Add a variable to denote NA
[guide]

[demo]

2.2 Outliers

Detect by Arbitrary Boundary
[guide]

[demo]

Detect by Mean & Standard Deviation
[guide]

[demo]

Detect by IQR
[guide]

[demo]

Detect by MAD
[guide]

[demo]

Mean/Median/Mode Imputation
[guide]

[demo]

Discretization
[guide]

[demo]

Imputation with Arbitrary Value
[guide]

[demo]

Windsorization
[guide]

[demo]

Discard Outliers
[guide]

[demo]

2.3 Rare Values

Mode Imputation
[guide]

[demo]

Grouping into One New Category
[guide]

[demo]

2.4 High Cardinality

Grouping Labels with Business Understanding
[guide]

Grouping Labels with Rare Occurrence into One Category
[guide]

[demo]

Grouping Labels with Decision Tree
[guide]

[demo]

3. Feature Engineering

3.1 Feature Scaling

Normalization - Standardization
[guide]

[demo]

Min-Max Scaling
[guide]

[demo]

Robust Scaling
[guide]

[demo]

3.2 Discretize

Equal Width Binning
[guide]

[demo]

Equal Frequency Binning
[guide]

[demo]

K-means Binning
[guide]

[demo]

Discretization by Decision Trees
[guide]

[demo]

ChiMerge
[guide]

[demo]

3.3 Feature Encoding

One-hot Encoding
[guide]

[demo]

Ordinal-Encoding
[guide]

[demo]

Count/frequency Encoding
[guide]

Mean Encoding
[guide]

[demo]

WOE Encoding
[guide]

[demo]

Target Encoding
[guide]

[demo]

3.4 Feature Transformation

Logarithmic Transformation
[guide]

[demo]

Reciprocal Transformation
[guide]

[demo]

Square Root Transformation
[guide]

[demo]

Exponential Transformation
[guide]

[demo]

Box-cox Transformation
[guide]

[demo]

Quantile Transformation
[guide]

[demo]

3.5 Feature Generation

Missing Data Derived
[guide]

[demo]

Simple Stats
[guide]

Crossing
[guide]

Ratio & Proportion
[guide]

Cross Product
[guide]

Polynomial
[guide]

[demo]

Feature Learning by Tree
[guide]

[demo]

Feature Learning by Deep Network
[guide]

4. Feature Selection

4.1 Filter Method

Variance
[guide]

[demo]

Correlation
[guide]

[demo]

Chi-Square
[guide]

[demo]

Mutual Information Filter
[guide]

[demo]

Information Value (IV)
[guide]

4.2 Wrapper Method

Forward Selection
[guide]

[demo]

Backward Elimination
[guide]

[demo]

Exhaustive Feature Selection
[guide]

[demo]

Genetic Algorithm
[guide]

4.3 Embedded Method

Lasso (L1)
[guide]

[demo]

Random Forest Importance
[guide]

[demo]

Gradient Boosted Trees Importance
[guide]

[demo]

4.4 Feature Shuffling

Random Shuffling
[guide]

[demo]

4.5 Hybrid Method

Recursive Feature Selection
[guide]

[demo]

Recursive Feature Addition
[guide]

[demo]

Key Links and Resources

Feature Engineering for Machine Learning online course

https://www.trainindata.com/p/feature-engineering-for-machine-learning

Feature Selection for Machine Learning online course

https://www.trainindata.com/p/feature-selection-for-machine-learning

JMLR Special Issue on Variable and Feature Selection

http://jmlr.org/papers/special/feature03.html

Data Analysis Using Regression and Multilevel/Hierarchical Models, Chapter 25: Missing data

http://www.stat.columbia.edu/~gelman/arm/missing.pdf

Data mining and the impact of missing data

http://core.ecu.edu/omgt/krosj/IMDSDataMining2003.pdf

PyOD: A Python Toolkit for Scalable Outlier Detection

https://github.com/yzhao062/pyod

Weight of Evidence (WoE) Introductory Overview

http://documentation.statsoft.com/StatisticaHelp.aspx?path=WeightofEvidence/WeightofEvidenceWoEIntroductoryOverview

About Feature Scaling and Normalization

http://sebastianraschka.com/Articles/2014_about_feature_scaling.html

Feature Generation with RF, GBDT and Xgboost

https://blog.csdn.net/anshuai_aw1/article/details/82983997

A review of feature selection methods with applications

https://ieeexplore.ieee.org/iel7/7153596/7160221/07160458.pdf

About

Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself.

Topics

data-science

machine-learning

data-mining

deep-learning

scikit-learn

data-visualization

feature-selection

feature-extraction

data-analysis

data-scientists

feature-engineering

features

feature-scaling

Resources

Readme

Uh oh!

There was an error while loading.
Please reload this page
.

Activity

Stars

764

stars

Watchers

14

watching

Forks

275

forks

Report repository

Releases

No releases published

Packages

0

No packages published

Uh oh!

There was an error while loading.
Please reload this page
.

Contributors

3

Uh oh!

There was an error while loading.
Please reload this page
.

Languages

Jupyter Notebook

91.8%

Python

8.2%

---

## Metadata

**Source:** [https://github.com/ashishpatel26/Amazing-Feature-Engineering](https://github.com/ashishpatel26/Amazing-Feature-Engineering)
**Type:** github-repo
**Extracted:** 2026-01-18T12:45:28.766470
**Extractor:** fallback
**Word Count:** 1194
