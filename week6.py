import pandas as pd

# load csv
sold = pd.read_csv(
    "CRMLSSold_Cleaned.csv",
    low_memory=False,
    encoding="latin1"
)

# ensure numeric
numeric_columns = [
    "ClosePrice",
    "OriginalListPrice",
    "LivingArea",
    "DaysOnMarket"
]

for column in numeric_columns:
    sold[column] = pd.to_numeric(
        sold[column],
        errors="coerce"
    )

# ensure datetime
date_columns = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate"
]

for column in date_columns:
    sold[column] = pd.to_datetime(
        sold[column],
        errors="coerce",
        utc=True
    )

# close / original listing ratio
sold["price_ratio"] = (
    sold["ClosePrice"] /
    sold["OriginalListPrice"]
)

sold["close_to_original_list_ratio"] = (
    sold["ClosePrice"] /
    sold["OriginalListPrice"]
)

# price / ft^2
sold["price_per_sqft"] = (
    sold["ClosePrice"] /
    sold["LivingArea"]
)

sold["days_on_market_metric"] = sold["DaysOnMarket"]

# close date time fields
sold["year"] = sold["CloseDate"].dt.year
sold["month"] = sold["CloseDate"].dt.month
sold["YrMo"] = sold["CloseDate"].dt.to_period("M").astype(str)

# days from listing to accepted contract
sold["listing_to_contract_days"] = (
    sold["PurchaseContractDate"] -
    sold["ListingContractDate"]
).dt.days

# days from accepted contract to closing
sold["contract_to_close_days"] = (
    sold["CloseDate"] -
    sold["PurchaseContractDate"]
).dt.days

# replace invalid div dates
sold.loc[
    sold["OriginalListPrice"] <= 0,
    ["price_ratio", "close_to_original_list_ratio"]
] = pd.NA

sold.loc[
    sold["LivingArea"] <= 0,
    "price_per_sqft"
] = pd.NA

# print sample
engineered_columns = [
    "ClosePrice",
    "OriginalListPrice",
    "LivingArea",
    "price_ratio",
    "close_to_original_list_ratio",
    "price_per_sqft",
    "days_on_market_metric",
    "year",
    "month",
    "YrMo",
    "listing_to_contract_days",
    "contract_to_close_days"
]
print("sample:")
print(sold[engineered_columns].head(10))

# segmented summary by county
county_summary = (
    sold.groupby("CountyOrParish")
    .agg(
        transaction_count=("ClosePrice", "count"),
        median_close_price=("ClosePrice", "median"),
        average_close_price=("ClosePrice", "mean"),
        median_price_per_sqft=("price_per_sqft", "median"),
        average_days_on_market=("DaysOnMarket", "mean"),
        median_price_ratio=("price_ratio", "median")
    )
    .reset_index()
    .sort_values(
        "median_close_price",
        ascending=False
    )
)
print()
print("county summary:")
print(county_summary.head(20))

# save segmented
county_summary.to_csv(
    "County_Market_Summary.csv",
    index=False
)

# save altered dataset
sold.to_csv(
    "CRMLSSold_Feature_Engineered.csv",
    index=False
)
