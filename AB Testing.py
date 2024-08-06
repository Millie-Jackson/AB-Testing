import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import warnings
warnings.filterwarnings("ignore")



# Read in data
df = pd.read_csv("marketing_AB.csv")
#print(df)

# Ensure the ID column is unique, having no duplicates
df.duplicated(subset = 'user id').sum()

# Dropping unwanted columns
df.drop(['Unnamed: 0', 'user id'], axis = 1, inplace = True)
#print(df.columns)

# Check how many catagories are in each column
df_cat = df[['test group', 'converted', 'most ads day', 'most ads hour']]
#print(df_cat.nunique())

# Check the names of these levels make sense
for i in df_cat.columns:
    print(i.upper(), ":", df_cat[i].unique())



# UNIVARIATE ANALYSIS #
variable = 'test group' 

plt.figure(figsize = (6, 4))

# Count plot
plt.subplot(1, 2, 1) # Divide the figure so we can show both plots (1 row, 2 columns)
sns.countplot(x=variable, data=df_cat)
plt.title(f'Count Plot - {variable}')

# Pie Chart
plt.subplot(1, 2, 2) # Put it in the 2nd column
counts = df_cat[variable].value_counts()
plt.pie(counts, labels=counts.index, autopct='%0.2f%%')
plt.title(f'Pie Chart - {variable}')

# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture the conversion rate
variable = 'converted' 

plt.figure(figsize = (6, 4))

# Count plot
plt.subplot(1, 2, 1) # Divide the figure so we can show both plots (1 row, 2 columns)
sns.countplot(x=variable, data=df_cat)
plt.title(f'Count Plot - {variable}')

# Pie Chart
plt.subplot(1, 2, 2) # Put it in the 2nd column
counts = df_cat[variable].value_counts()
plt.pie(counts, labels=counts.index, autopct='%0.2f%%')
plt.title(f'Pie Chart - {variable}')

# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture the most ads per day
variable = 'most ads day' 

plt.figure(figsize = (6, 4))

# Count plot
plt.subplot(1, 2, 1) # Divide the figure so we can show both plots (1 row, 2 columns)
sns.countplot(x=variable, data=df_cat, order = df_cat['most ads day'].value_counts().index) # Order by decreasing value
plt.title(f'Count Plot - {variable}')
plt.xticks(rotation = 90) # Rotate so the words dont overlap the plot

# Pie Chart
plt.subplot(1, 2, 2) # Put it in the 2nd column
counts = df_cat[variable].value_counts()
plt.pie(counts, labels=counts.index, autopct='%0.2f%%')
plt.title(f'Pie Chart - {variable}')

# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture most ads hour
variable = 'most ads hour' 

plt.figure(figsize = (6, 4))

# Count plot
plt.subplot(1, 2, 1) # Divide the figure so we can show both plots (1 row, 2 columns)
sns.countplot(x=variable, data=df_cat, order = df_cat['most ads hour'].value_counts().index) # Order by decreasing value
plt.title(f'Count Plot - {variable}')
plt.xticks(rotation = 90) # Rotate so the words dont overlap the plot

# Pie Chart
plt.subplot(1, 2, 2) # Put it in the 2nd column
counts = df_cat[variable].value_counts()
plt.pie(counts, labels=counts.index, autopct='%0.2f%%')
plt.title(f'Pie Chart - {variable}')

# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Finally, total ads
variable = 'total ads' 

plt.figure(figsize = (6, 4))

# Histogram
plt.subplot(1, 2, 1) # Divide the figure so we can show both plots (1 row, 2 columns)
sns.histplot(x=variable, data = df[df['total ads'] < 50]) # Choosing the top 50% to reduce the outliers
plt.title(f'Histogram - {variable}')
plt.xticks(rotation = 90) # Rotate so the words dont overlap the plot

# Box Plot
plt.subplot(1, 2, 2) # Put it in the 2nd column
sns.boxplot(y = variable, data = df[df['total ads'] < 50]) # Choosing the top 50% to reduce the outliers
plt.title(f'Box Plot- {variable}')

# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()

# Checking the descriptive stats
df['total ads'].describe()



# BIVARIATE ANALYSIS #

# Compare 'test group' to 'converted'
ct_conversion_test_group = pd.crosstab(df['test group'], df['converted'], normalize = 'index') # normalise (divide by rows)
print(ct_conversion_test_group)
ct_conversion_test_group.plot.bar(stacked = True);

# Compare 'most ads day' to 'converted'
ct_conversion_day = pd.crosstab(df['most ads day'], df['converted'], normalize = 'index') # normalise (divide by rows)
print(ct_conversion_day.sort_values(by = True, ascending = False))
ct_conversion_day.plot.bar(stacked = True);

# Compare 'most ads hour' to 'converted'
ct_conversion_hour = pd.crosstab(df['most ads hour'], df['converted'], normalize = 'index') # normalise (divide by rows)
print(ct_conversion_hour.sort_values(by = True, ascending = False))
ct_conversion_hour.plot.bar(stacked = True);

# Compare 'converted' to ;total ads'
sns.boxplot(x = 'converted', y = 'total ads', data = df[df['total ads'] < 50]); # Choosing the top 50% to reduce the outliers

plt.show()



# STATISTICAL TESTS #
from scipy.stats import chi2_contingency
alpha = 0.5
# Dont compare 'converted' to 'converted'
for variable in df_cat.columns:
    if variable != 'converted':
        # Create a contingency table (cross-tabulation)
        contingency_table = pd.crosstab(df_cat[variable], df_cat['converted'])

        # Perform chi_squared test
        chi2, p, _, _ = chi2_contingency(contingency_table)

        # Display results
        print(f"\nChi-squared test for {variable} vs.converted:")
        print(f"Chi-squared value: {chi2}")
        print(f"p-value: {p}")

        # Check for significance 
        if p < alpha:
            print(f"The difference in conversion rates across {variable} is statistically significant.")
        else:
            print(f"There is no significant difference in conversion rates across {variable}.")



# HYPOTHISIS TESTING #
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu

# Step 1: Check Assumption
# Normality assumption
shapiro_stat_true, shapiro_p_value_true = shapiro(df[df['converted'] == True]['total ads'])
shapiro_stat_false, shapiro_p_value_false = shapiro(df[df['converted'] == False]['total ads'])

print(f"Shapiro-Wilk test for normality (True group): p-value = {shapiro_p_value_true}")
print(f"Shapiro-Wilk test for normality (False group): p-value = {shapiro_p_value_false}")

# Equality of varience assumptions
levene_stat, levene_p_value = levene(df[df['converted']]['total ads'], df[~df['converted']]['total ads'])
print(f"Levene's test for equality of variances: p-value = {levene_p_value}")

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