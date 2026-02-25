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



# =========================
# CLIENT-FACING CHARTS
# =========================

# Helper: trim extreme outliers for clearer plots (client-friendly)
ads_cap = df["total ads"].quantile(0.95)
df_plot = df[df["total ads"] <= ads_cap].copy()

# 1) Conversion rate: Ad vs PSA (the headline chart)
conv_rate = df.groupby("test group")["converted"].mean().sort_index() * 100  # %
plt.figure(figsize=(6, 4))
bars = plt.bar(conv_rate.index, conv_rate.values)
plt.ylabel("Conversion rate (%)")
plt.title("Conversion Rate: Ad vs Control (PSA)")
plt.ylim(0, max(conv_rate.values) * 1.6)

for b in bars:
    y = b.get_height()
    plt.text(b.get_x() + b.get_width()/2, y, f"{y:.2f}%", ha="center", va="bottom")

plt.tight_layout()
plt.show()

# Optional: print uplift in plain English
ad = conv_rate.get("ad", np.nan)
psa = conv_rate.get("psa", np.nan)
if pd.notna(ad) and pd.notna(psa):
    print(f"Ad conversion:  {ad:.2f}%")
    print(f"PSA conversion: {psa:.2f}%")
    print(f"Absolute uplift: {ad - psa:.2f} percentage points")

# 2) Exposure vs conversion (boxplot)
data_false = df_plot[df_plot["converted"] == False]["total ads"]
data_true  = df_plot[df_plot["converted"] == True]["total ads"]

plt.figure(figsize=(6, 4))
plt.boxplot([data_false, data_true], labels=["Not converted", "Converted"], showfliers=False)
plt.ylabel("Total ads seen (trimmed)")
plt.title("Ad Exposure by Conversion Status")
plt.tight_layout()
plt.show()

# 3) OPTIONAL: Conversion rate by hour (only if you want 1 timing chart)
# Keeps it readable by sorting by conversion rate and showing top 10 hours
conv_by_hour = (df.groupby("most ads hour")["converted"].mean() * 100).sort_values(ascending=False).head(10)

plt.figure(figsize=(8, 4))
bars = plt.bar(conv_by_hour.index.astype(str), conv_by_hour.values)
plt.ylabel("Conversion rate (%)")
plt.title("Top 10 Hours by Conversion Rate")
plt.xticks(rotation=45)

for b in bars:
    y = b.get_height()
    plt.text(b.get_x() + b.get_width()/2, y, f"{y:.2f}%", ha="center", va="bottom")

plt.tight_layout()
plt.show()

import os

# =========================
# CLIENT-FACING CHARTS
# =========================

# Create figures folder if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Trim extreme outliers (cleaner presentation)
ads_cap = df["total ads"].quantile(0.95)
df_plot = df[df["total ads"] <= ads_cap].copy()

# -------------------------
# 1️⃣ Conversion Rate: Ad vs PSA
# -------------------------

conv_rate = df.groupby("test group")["converted"].mean() * 100

plt.figure(figsize=(6, 4))
bars = plt.bar(conv_rate.index, conv_rate.values)
plt.ylabel("Conversion Rate (%)")
plt.title("Conversion Rate: Ad vs Control")
plt.ylim(0, max(conv_rate.values) * 1.6)

for b in bars:
    y = b.get_height()
    plt.text(
        b.get_x() + b.get_width()/2,
        y,
        f"{y:.2f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("figures/conversion_rate_ad_vs_control.png", dpi=300)
plt.close()


# -------------------------
# 2️⃣ Ad Exposure vs Conversion
# -------------------------

data_false = df_plot[df_plot["converted"] == False]["total ads"]
data_true  = df_plot[df_plot["converted"] == True]["total ads"]

plt.figure(figsize=(6, 4))
plt.boxplot(
    [data_false, data_true],
    labels=["Not Converted", "Converted"],
    showfliers=False
)
plt.ylabel("Total Ads Seen (Trimmed)")
plt.title("Ad Exposure by Conversion Status")

plt.tight_layout()
plt.savefig("figures/ad_exposure_vs_conversion.png", dpi=300)
plt.close()


# -------------------------
# 3️⃣ OPTIONAL: Top 10 Hours by Conversion
# -------------------------

conv_by_hour = (
    df.groupby("most ads hour")["converted"]
    .mean()
    .sort_values(ascending=False)
    .head(10) * 100
)

plt.figure(figsize=(8, 4))
bars = plt.bar(conv_by_hour.index.astype(str), conv_by_hour.values)
plt.ylabel("Conversion Rate (%)")
plt.title("Top 10 Hours by Conversion Rate")
plt.xticks(rotation=45)

for b in bars:
    y = b.get_height()
    plt.text(
        b.get_x() + b.get_width()/2,
        y,
        f"{y:.2f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("figures/top_hours_conversion.png", dpi=300)
plt.close()

print("Charts saved to /figures folder.")



# UNIVARIATE ANALYSIS #
variable = 'test group' 

plt.figure(figsize = (6, 4))


# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture the conversion rate
variable = 'converted' 

plt.figure(figsize = (6, 4))


# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture the most ads per day
variable = 'most ads day' 

plt.figure(figsize = (6, 4))


# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Capture most ads hour
variable = 'most ads hour' 

plt.figure(figsize = (6, 4))


# Adust layout
plt.tight_layout() #  Display the plots nicely
#plt.show()



# Finally, total ads
variable = 'total ads' 

plt.figure(figsize = (6, 4))


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