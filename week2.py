import pandas as pd
import matplotlib.pyplot as plt

# loading datasets
sold = pd.read_csv(
    "CRMLSSold_Combined.csv", 
    low_memory = False,
    encoding = "latin1"
)

listing = pd.read_csv(
    "CRMLSListing_Combined.csv",
    low_memory = False,
    encoding = "latin1"
)
 
# dataset info
print("dataset info -------------------------")
print()
print("rows, columns:")
print(sold.shape)
print("column names:")
print(sold.columns)
print("data types:")
print(sold.dtypes)
print("first 5 rows:")
print(sold.head())
print()

# property types & count
print("property types and count -------------------------")
print()
print("unique property types:")
print(sold["PropertyType"].unique())
print("count property type:")
print(sold["PropertyType"].value_counts())
print()

# res filter
print("filter -------------------------")
print()
sold_residential = sold[sold["PropertyType"] == "Residential"]
print("rows after filter:")
print(len(sold_residential))
print()

# missing values & count
print("missing values and count -------------------------")
print()
missing = sold_residential.isnull().sum()
missing_percent = (sold_residential.isnull().mean() * 100)
missing_summary = pd.DataFrame({
    "missing count": missing,
    "missing percent": missing_percent
})
print("missing summary:")
print(missing_summary)
print("columns missing > 90%:")
print(missing_summary[missing_summary["missing percent"] > 90])
print()

# numeric summary
print("numeric summary -------------------------")
print()
numeric_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]

# ensure columns are numbers
for column in numeric_columns:
    sold_residential[column] = pd.to_numeric(
        sold_residential[column],
        errors="coerce"
    )

for column in numeric_columns:
    print(column)
    print(sold_residential[column].describe())
    print("median:")
    print(sold_residential[column].median())
    print()

sold_residential.to_csv("CRMLSSold_Validated.csv", index=False)

# plots
print("plots -------------------------")
print()
for column in numeric_columns:
    clean_col = sold_residential[column].dropna()
    clipped = clean_col[
        clean_col <= clean_col.quantile(0.99)
    ]
    clipped.hist(bins=50)
    plt.title(f"{column} histogram (clipped at 99th percentile)")
    plt.savefig(f"{column}_histogram.png")
    plt.close()

    clipped.to_frame().boxplot(column=column)
    plt.title(f"{column} boxplot (clipped at 99th percentile)")
    plt.savefig(f"{column}_boxplot.png")
    plt.close()

# calculating outliers
print("potential outliers -------------------------")
print()
for column in numeric_columns:
    q1 = sold_residential[column].quantile(0.25)
    q3 = sold_residential[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = sold_residential[
        (sold_residential[column] < lower) |
        (sold_residential[column] > upper)
    ]
    print(f"num of {column} outliers: {len(outliers)}")

