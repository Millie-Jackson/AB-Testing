# A/B Testing Analysis – Marketing Campaign Evaluation

## Executive Summary
- The advertisement group achieved a higher conversion rate than the control group (PSA).
- The uplift in conversion was statistically significant.
- Conversion likelihood increased with higher ad exposure.
- Time of day and day of week influenced performance.
- Findings support continued ad spend with optimisation of timing and exposure frequency.

## Overview
A marketing team requested an independent analysis of their A/B testing campaign to determine whether paid advertisements were driving meaningful increases in conversion rates compared to a control (PSA/no ad).

The objective was to validate performance, quantify uplift, and assess whether observed differences were statistically significant before scaling ad spend.

## Business Questions
1. Did the advertisement increase conversions?
2. Was the uplift statistically significant?
3. Are timing and frequency factors influencing performance?
4. Can we estimate the potential impact on revenue?

## Approach

### Data Preparation
- Verified user ID uniqueness
- Removed irrelevant fields
- Checked for missing values and anomalies
- Prepared data for statistical comparison

### Exploratory Analysis
- Compared conversion rates between control and ad groups
- Examined performance by day and hour
- Analysed distribution of total ads viewed
- Identified outliers and class imbalance

### Statistical Testing
- Chi-squared tests for categorical relationships
- Normality and variance testing (Shapiro-Wilk, Levene)
- Mann-Whitney U test where assumptions failed
- Validation of conversion uplift significance

## Key Findings
- The advertisement group showed a higher conversion rate than the control group.
- The difference was statistically significant.
- Day and hour of exposure influenced conversion performance.
- Users who converted were exposed to more ads on average.
- Data exhibited class imbalance, which was accounted for in modelling considerations.

## Outcome
The analysis confirmed that ad exposure contributed to increased conversions and that the uplift was statistically reliable.
Clear recommendations were provided to:

- Optimise ad timing
- Evaluate exposure thresholds
- Improve campaign efficiency
- Support budget allocation decisions

## Tools Used
Python · Pandas · SciPy · Matplotlib · Seaborn
Statistical testing · A/B testing methodology · Data visualisation


  
**- Analyze the distribution of continuous variables using histograms and box plots.**
![image](https://github.com/user-attachments/assets/5d5a7331-71ab-49d9-8dbe-604fb5714e64)
- The median on the box plot is 10 ads

**- Calculate descriptive statistics.**
```  
  converted      False      True
test group

ad               0.974453  0.025547
psa              0.982146  0.017854
converted        False     True
```
27 is the 75% percentile lets take the top 50% because most of it is outliers

### Bivariate Analysis:
**- Use crosstabulation and bar plots to compare conversion rates between different groups (e.g., test group, most ads day, most ads hour).**
![image](https://github.com/user-attachments/assets/91c1098e-7939-40e7-8e87-fd75edf49199)
- Out of all the people that saw the ad, 2.5% made a purchase
- Out of all the people that saw the general announcement, only 1.7% made a purchase
![image](https://github.com/user-attachments/assets/f49cefba-7f34-4abb-b3ef-4982c3bfcc32)
- most ads day = Friday is when most conversions happen
**- Use box plots to compare the total number of ads seen by converted and non-converted users.**
![image](https://github.com/user-attachments/assets/f1847971-be28-454f-b95d-1c3c71644227)
- Median amount of ads screen by converters is 25 vs 10 by those not converted

## 3. Statistical Tests
- Perform Chi-squared tests to evaluate the significance of differences in conversion rates across different groups.
```
Chi-squared test for test group vs.converted:
Chi-squared value: 54.005823883685245
p-value: 1.9989623063390075e-13
The difference in conversion rates across test group is statistically significant.

Chi-squared test for most ads day vs.converted:
Chi-squared value: 410.0478857936585
p-value: 1.932184379244731e-85
The difference in conversion rates across most ads day is statistically significant.

Chi-squared test for most ads hour vs.converted:
Chi-squared value: 430.76869230822086
p-value: 8.027629823696771e-77
```
**test group vs converted** = Showing the ad makes a difference

**most ads day vs converted** = the day of the week the ad is shown makes a difference

**most ads hour vs converted** = the hour of the day the ad is shown makes a difference


- Conduct hypothesis testing. Check for normality using the Shapiro-Wilk test.
```
# Step 1: Check Assumption
# Normality assumption
shapiro_stat_true, shapiro_p_value_true = shapiro(df[df['converted'] == True]['total ads'])
shapiro_stat_false, shapiro_p_value_false = shapiro(df[df['converted'] == False]['total ads'])

print(f"Shapiro-Wilk test for normality (True group): p-value = {shapiro_p_value_true}")
print(f"Shapiro-Wilk test for normality (False group): p-value = {shapiro_p_value_false}")
```

- Check for equality of variances using Levene's test.
```
# Equality of varience assumptions
levene_stat, levene_p_value = levene(df[df['converted']]['total ads'], df[~df['converted']]['total ads'])
print(f"Levene's test for equality of variances: p-value = {levene_p_value}")
```
- Depending on the test results, perform either a t-test for means or a Mann-Whitney U test for medians.
```
# Step 2: Perform a suitable test
alpha = 0.05

if shapiro_p_value_true > alpha and shapiro_p_value_false> alpha and levene_p_value > alpha:
    # Assumptions met - use t-test for means
    t_stat, t_p_value = ttest_ind(df[df['converted']]['total ads'], df[~df['converted']]['total ads'])
    print(f"Independent two-sample t_test: p-value = {t_p_value}")
else:
    # Assumptions not met - use Mann-Whitney U test for medians
    u_stat, u_p_value, = mannwhitneyu(df[df['converted']]['total ads'], df[~df['converted']]['total ads'])
    print(f"Mann-Whitney U test: p-value = {u_p_value}")
```

```
The difference in conversion rates across most ads hour is statistically significant.
Shapiro-Wilk test for normality (True group): p-value = 0.0
Shapiro-Wilk test for normality (False group): p-value = 0.0
Levene's test for equality of variances: p-value = 0.0
Mann-Whitney U test: p-value = 0.0
```
Conversion status is related to, how many median ads they have seen, so it does make a difference

### Machine Learning
In the classification report it has been noted that the support for each class is unbalanced.
```
          support

False     171970
True      4461
```
Building machine learning models on unbalanced data is a common and often necessary practice in many real-world applications, such as fraud detection, medical diagnosis, and rare event prediction. While it poses challenges, there are strategies and techniques to effectively handle unbalanced data and create robust models.


