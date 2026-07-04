import pandas as pd
import glob

# sold
sold_files = sorted(glob.glob("csv/CRMLSSold*.csv"))
sold_dfs = [pd.read_csv(file, low_memory=False, encoding='latin1') for file in sold_files]

print("sold before concat:", sum(len(dfs) for dfs in sold_dfs))
sold = pd.concat(sold_dfs, ignore_index=True)
print("sold after concat:", len(sold))

print("sold before residential:", len(sold))
sold_residential = sold[sold["PropertyType"] == "Residential"]
print("sold after residential:", len(sold_residential))

sold.to_csv(
    "CRMLSSold_Combined.csv",
    index=False
)
sold_residential.to_csv(
    "CRMLSSold_Combined_Residential.csv",
    index=False
)

# listing
listing_files = sorted(glob.glob("csv/CRMLSListing*.csv"))
listing_dfs = [pd.read_csv(file, low_memory=False, encoding='latin1') for file in listing_files]

print("listing before concat:", sum(len(dfs) for dfs in listing_dfs))
listing = pd.concat(listing_dfs, ignore_index=True)
print("listing after concat:", len(listing))

print("listing before residential:", len(listing))
listing_residential = listing[listing["PropertyType"] == "Residential"]
print("listing after residential:", len(listing_residential))

listing.to_csv(
    "CRMLSListing_Combined.csv",
    index=False
)
listing_residential.to_csv(
    "CRMLSListing_Combined_Residential.csv",
    index=False
)