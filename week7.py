import pandas as pd

# load
sold = pd.read_csv("CRMLSSold_Cleaned.csv", low_memory=False, encoding="latin1")
print(sold["PropertyType"].value_counts())

numeric_columns = ["ClosePrice", "LivingArea", "DaysOnMarket"]

def flagOutliers(df, column): 
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    flagName = f"{column}_outlier_flag"
    df[flagName] = ((df[column] < lower) | (df[column] > upper))
    print("----------------------------------------------------------------------")
    print(column)
    print(f"q1: {Q1}")
    print(f"q3: {Q3}")
    print(f"iqr: {IQR}")
    print(f"lower bound: {lower}")
    print(f"upper bound: {upper}")
    print(f"flagged outliers: {df[flagName].sum()}")
    return df

for column in numeric_columns:
    sold = flagOutliers(sold, column)

sold_filtered = sold[~sold["ClosePrice_outlier_flag"] & ~sold["LivingArea_outlier_flag"] 
                    & ~sold["DaysOnMarket_outlier_flag"]].copy()

# comparisons
print()
print("dataset comparisons ----------------------------------------------------------------------")
print(f"rows before filtering: {len(sold)}")
print(f"rows after filtering:  {len(sold_filtered)}")
print(f"rows removed:          {len(sold) - len(sold_filtered)}")
print()
for column in numeric_columns:
    print(column)
    print("median before filtering:")
    print(sold[column].median())
    print("median after filtering:")
    print(sold_filtered[column].median())
    print()
for column in numeric_columns:
    print(column)
    print("before filtering:")
    print(sold[column].describe(percentiles=[0.01, 0.25, 0.50, 0.75, 0.99]))
    print()
    print("after filtering:")
    print(sold_filtered[column].describe(percentiles=[0.01, 0.25, 0.50, 0.75, 0.99]))
    print()

# save new datasets
sold.to_csv("CRMLSSold_Outliers_Flagged.csv", index=False)
sold_filtered.to_csv("CRMLSSold_Outliers_Filtered.csv", index=False)
