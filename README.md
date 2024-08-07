# Overview
This project focuses on analyzing a marketing A/B testing dataset to evaluate the effectiveness of advertising campaigns. Marketing companies often use A/B testing to compare different strategies and determine which one has the most significant impact on their business metrics. This project aims to answer key questions regarding the success of marketing campaigns and the specific impact of ads on conversion rates.

# Objectives
The main objectives of this project are to:

Determine if the marketing campaign was successful.
Assess how much of the campaign's success can be attributed to the ads.
By conducting an A/B test, we can compare the conversion rates between an experimental group exposed to ads and a control group that sees a Public Service Announcement (PSA) or no ad at all. The goal is to analyze these groups to find out if the ads were successful, estimate the potential revenue from the ads, and evaluate the statistical significance of the differences between the groups.

# Dataset
The dataset is designed to analyze the groups, determine if the ads were successful, estimate the revenue generated from the ads, 
and assess if the difference between the groups is statistically significant.

## Data Dictionary
**Index:** Row index

**user id:** Unique identifier for each user

**test group:** Indicates whether the user saw the advertisement ("ad") or the public service announcement ("psa")

**converted:** Indicates whether the user bought the product (True) or not (False)

**total ads:** The total number of ads seen by the user

**most ads day:** The day on which the user saw the highest number of ads

**most ads hour:** The hour of the day during which the user saw the highest number of ads.

## Usage
This dataset allows for comprehensive analysis of the effectiveness of marketing campaigns through A/B testing, 
helping companies to make data-driven decisions and optimize their marketing strategies.

# Skills Demonstrated

**A/B Testing:** The project involves comparing the conversion rates between different groups (test groups) to assess the impact of different variables, 
which is a core part of A/B testing.

**Data Visualization:** The project extensively uses data visualization techniques such as count plots, pie charts, histograms, 
and box plots to visualize the distribution of different variables and their relationships.

**Exploratory Data Analysis (EDA):** The project performs univariate and bivariate analysis, including descriptive statistics and visualization to understand t
he data distribution and relationships between variables.

**Hypothesis Testing:** The project uses statistical tests (Chi-squared test, Shapiro-Wilk test, Levene's test, t-test, and Mann-Whitney U test) 
to test hypotheses about the differences in conversion rates across different groups and variables.

# Project Steps
## 1. Data Preparation
**- Load the dataset.**
**- Ensure the uniqueness of the user ID column by checking for duplicates.**
**- Drop unwanted columns.**
**- Check for missing values**
```
# Read in data
df = pd.read_csv("marketing_AB.csv")
print(df)

# Ensure the ID column is unique, having no duplicates
df.duplicated(subset = 'user id').sum()

# Dropping unwanted columns
df.drop(['Unnamed: 0', 'user id'], axis = 1, inplace = True)
print(df.columns)

# Check how many catagories are in each column
df_cat = df[['test group', 'converted', 'most ads day', 'most ads hour']]
print(df_cat.nunique())

# Check the names of these levels make sense
for i in df_cat.columns:
    print(i.upper(), ":", df_cat[i].unique())

# Check for missing values
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values)
```
## 2. Exploratory Data Analysis (EDA)
### Univariate Analysis:
**- Visualize the distribution of categorical variables using count plots and pie charts.**
![image](https://github.com/user-attachments/assets/bdc6ec81-eb0e-45d0-9571-3ae0a319103b)
- The count plot is difficult to read
- 4% of people were shown the public service announcement
![image](https://github.com/user-attachments/assets/e6574480-e258-4235-ad1b-96214c2b3e8c)
- Only 2.52% of the public service announcement converted
![image](https://github.com/user-attachments/assets/47484e73-6d70-4c08-bd99-c18918717f64)
- The pie chart is not confusing, too many categories
- Count plot shows Friday is most popular followed by Monday
![image](https://github.com/user-attachments/assets/ae8bfa86-019c-46b4-9739-73f352196913)
- Again the pie chart is useless now, too many categories
- Early hours of the day (after midnight) are the least effective
  
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
![image](https://github.com/user-attachments/assets/3294c42c-2464-4992-bc0f-04c6e5ccf76a)
- most ads hour = Most conversions at 1600 then 2000 then 1500. Least conversions at 0200, 0300, 0100. This makes sense.
- This shows us when people are most likely to buy
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

# IN PROGRESS



Results
The analysis provides insights into:

The success rate of the marketing campaign.
The impact of ads on conversion rates.
Statistical significance of the differences observed between the experimental and control groups.
Conclusion
This project demonstrates how A/B testing and statistical analysis can be applied to evaluate the effectiveness of marketing campaigns. By analyzing the dataset, we can make data-driven decisions to optimize marketing strategies and improve business outcomes.

Getting Started
Prerequisites
Python 3.x
Required Python libraries: numpy, pandas, matplotlib, seaborn, scipy
Installation
Install the required libraries using pip:

bash
Copy code
pip install numpy pandas matplotlib seaborn scipy
Running the Project
Clone the repository.
Navigate to the project directory.
Run the Jupyter notebook or Python script containing the project code.
bash
Copy code
jupyter notebook Marketing_AB_Testing.ipynb
# or
python marketing_ab_testing.py
Contact
For any questions or feedback, please contact [Your Name] at [Your Email].
