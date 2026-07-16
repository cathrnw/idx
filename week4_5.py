import pandas as pd

# load data
sold = pd.read_csv(
    "CRMLSSold_Combined_With_Mortgage_Rates.csv",
    low_memory=False,
    encoding="latin1"
)
listings = pd.read_csv(
    "CRMLSListing_Combined_With_Mortgage_Rates.csv",
    low_memory=False,
    encoding="latin1"
)
sold_rows_before = len(sold)
listing_rows_before = len(listings)

sold_columns_before = sold.shape[1]
listing_columns_before = listings.shape[1]

# convert date fields to datetime
date_columns = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]
for column in date_columns:
    if column in sold.columns:
        sold[column] = pd.to_datetime(sold[column], errors = "coerce", utc=True)
    if column in listings.columns:
        listings[column] = pd.to_datetime(listings[column], errors="coerce", utc=True)

# numeric data types
numeric_columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "Latitude",
    "Longitude",
    "rate_30yr_fixed"
]

for column in numeric_columns:
    if column in sold.columns:
        sold[column] = pd.to_numeric(sold[column], errors="coerce")
    if column in listings.columns:
        listings[column] = pd.to_numeric(listings[column], errors="coerce")

# missing values
def missing_value_report(df, threshold=90):
    missing = df.isnull().sum()
    missing_percent = df.isnull().mean() * 100
    missing_summary = pd.DataFrame({"missing count": missing, "missing percent": missing_percent})
    high_missing_columns = missing_summary[missing_summary["missing percent"] > threshold].index.tolist()
    return missing_summary, high_missing_columns

sold_missing_summary, sold_columns_to_drop = missing_value_report(
    sold,
    threshold=90
)
listing_missing_summary, listing_columns_to_drop = missing_value_report(
    listings,
    threshold=90
)

print("sold missing values report ----------------------------------------------------------------------")
print(sold_missing_summary)
print("sold columns above 90% missing:")
print(sold_columns_to_drop)
print()
print("listing missing values report -------------------------------------------------------------------")
print(listing_missing_summary)
print("listing columns above 90% missing:")
print(listing_columns_to_drop)
print()

# saving missing value reports
sold_missing_summary.to_csv(
    "CRMLSSold_Missing_Value_Report.csv"
)

listing_missing_summary.to_csv(
    "CRMLSListing_Missing_Value_Report.csv"
)

# drop columns > 90% missing
sold = sold.drop(
    columns=sold_columns_to_drop,
    errors="ignore"
)
listings = listings.drop(
    columns=listing_columns_to_drop,
    errors="ignore"
)
print("sold cols before dropping:", sold_columns_before)
print("sold cols after dropping:", sold.shape[1])
print("listing cols before dropping:", listing_columns_before)
print("listing cols after dropping:", listings.shape[1])
print()

# flag invalid numeric values
if "ClosePrice" in sold.columns:
    sold["invalid_close_price_flag"] = (
        sold["ClosePrice"].notna() &
        (sold["ClosePrice"] <= 0)
    )
if "LivingArea" in sold.columns:
    sold["invalid_living_area_flag"] = (
        sold["LivingArea"].notna() &
        (sold["LivingArea"] <= 0)
    )
if "DaysOnMarket" in sold.columns:
    sold["invalid_days_on_market_flag"] = (
        sold["DaysOnMarket"].notna() &
        (sold["DaysOnMarket"] < 0)
    )
if "BedroomsTotal" in sold.columns:
    sold["invalid_bedrooms_flag"] = (
        sold["BedroomsTotal"].notna() &
        (sold["BedroomsTotal"] < 0)
    )
if "BathroomsTotalInteger" in sold.columns:
    sold["invalid_bathrooms_flag"] = (
        sold["BathroomsTotalInteger"].notna() &
        (sold["BathroomsTotalInteger"] < 0)
    )
if "ListPrice" in listings.columns:
    listings["invalid_list_price_flag"] = (
        listings["ListPrice"].notna() &
        (listings["ListPrice"] <= 0)
    )
if "LivingArea" in listings.columns:
    listings["invalid_living_area_flag"] = (
        listings["LivingArea"].notna() &
        (listings["LivingArea"] <= 0)
    )
if "DaysOnMarket" in listings.columns:
    listings["invalid_days_on_market_flag"] = (
        listings["DaysOnMarket"].notna() &
        (listings["DaysOnMarket"] < 0)
    )
if "BedroomsTotal" in listings.columns:
    listings["invalid_bedrooms_flag"] = (
        listings["BedroomsTotal"].notna() &
        (listings["BedroomsTotal"] < 0)
    )
if "BathroomsTotalInteger" in listings.columns:
    listings["invalid_bathrooms_flag"] = (
        listings["BathroomsTotalInteger"].notna() &
        (listings["BathroomsTotalInteger"] < 0)
    )

# date consistency flags
sold["listing_after_close_flag"] = (
    sold["ListingContractDate"].notna() &
    sold["CloseDate"].notna() &
    (sold["ListingContractDate"] > sold["CloseDate"])
)
sold["purchase_after_close_flag"] = (
    sold["PurchaseContractDate"].notna() &
    sold["CloseDate"].notna() &
    (sold["PurchaseContractDate"] > sold["CloseDate"])
)
sold["negative_timeline_flag"] = (
    sold["ListingContractDate"].notna() &
    sold["PurchaseContractDate"].notna() &
    (sold["PurchaseContractDate"] < sold["ListingContractDate"])
)
listings["listing_after_close_flag"] = (
    listings["ListingContractDate"].notna() &
    listings["CloseDate"].notna() &
    (listings["ListingContractDate"] > listings["CloseDate"])
)
listings["purchase_after_close_flag"] = (
    listings["PurchaseContractDate"].notna() &
    listings["CloseDate"].notna() &
    (listings["PurchaseContractDate"] > listings["CloseDate"])
)
listings["negative_timeline_flag"] = (
    listings["ListingContractDate"].notna() &
    listings["PurchaseContractDate"].notna() &
    (
        listings["PurchaseContractDate"] <
        listings["ListingContractDate"]
    )
)
listings["listing_after_close_flag"] = (
    listings["ListingContractDate"].notna() &
    listings["CloseDate"].notna() &
    (listings["ListingContractDate"] > listings["CloseDate"])
)
listings["purchase_after_close_flag"] = (
    listings["PurchaseContractDate"].notna() &
    listings["CloseDate"].notna() &
    (listings["PurchaseContractDate"] > listings["CloseDate"])
)
listings["negative_timeline_flag"] = (
    listings["ListingContractDate"].notna() &
    listings["PurchaseContractDate"].notna() &
    (
        listings["PurchaseContractDate"] <
        listings["ListingContractDate"]
    )
)

# geographic data check
sold["missing_coordinates_flag"] = (
    sold["Latitude"].isna() |
    sold["Longitude"].isna()
)
sold["zero_coordinates_flag"] = (
    (sold["Latitude"] == 0) |
    (sold["Longitude"] == 0)
)
sold["positive_longitude_flag"] = (
    sold["Longitude"].notna() &
    (sold["Longitude"] > 0)
)
sold["implausible_coordinates_flag"] = (
    sold["Latitude"].notna() &
    sold["Longitude"].notna() &
    (
        (sold["Latitude"] < 32) |
        (sold["Latitude"] > 42.5) |
        (sold["Longitude"] < -125) |
        (sold["Longitude"] > -114)
    )
)
listings["missing_coordinates_flag"] = (
    listings["Latitude"].isna() |
    listings["Longitude"].isna()
)
listings["zero_coordinates_flag"] = (
    (listings["Latitude"] == 0) |
    (listings["Longitude"] == 0)
)
listings["positive_longitude_flag"] = (
    listings["Longitude"].notna() &
    (listings["Longitude"] > 0)
)
listings["implausible_coordinates_flag"] = (
    listings["Latitude"].notna() &
    listings["Longitude"].notna() &
    (
        (listings["Latitude"] < 32) |
        (listings["Latitude"] > 42.5) |
        (listings["Longitude"] < -125) |
        (listings["Longitude"] > -114)
    )
)

# clean data
sold_clean = sold[
    ~sold["invalid_close_price_flag"] &
    ~sold["invalid_living_area_flag"] &
    ~sold["invalid_days_on_market_flag"] &
    ~sold["invalid_bedrooms_flag"] &
    ~sold["invalid_bathrooms_flag"]
].copy()
listings_clean = listings[
    ~listings["invalid_list_price_flag"] &
    ~listings["invalid_living_area_flag"] &
    ~listings["invalid_days_on_market_flag"] &
    ~listings["invalid_bedrooms_flag"] &
    ~listings["invalid_bathrooms_flag"]
].copy()

# flagged dataset as new csv
sold.to_csv(
    "CRMLSSold_Flagged.csv",
    index=False
)
listings.to_csv(
    "CRMLSListing_Flagged.csv",
)

# clean dataset as new csv
sold_clean.to_csv(
    "CRMLSSold_Cleaned.csv",
    index=False
)
listings_clean.to_csv(
    "CRMLSListing_Cleaned.csv",
    index=False
)