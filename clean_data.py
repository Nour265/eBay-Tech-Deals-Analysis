import pandas as pd


# Load data

df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

# Ensure all string columns are stripped
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# Clean price and original_price columns

for col in ["price", "original_price"]:
    df[col] = (
        df[col]
        .fillna("")                         # handle NaN
        .str.replace("US", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    # replace empty strings with NaN for proper numeric conversion
    df[col] = df[col].replace("", pd.NA)


# Replace missing original_price with price

df["original_price"] = df.apply(
    lambda row: row["price"] if pd.isna(row["original_price"]) else row["original_price"],
    axis=1
)


# Clean shipping column

df["shipping"] = df["shipping"].fillna("").astype(str).str.strip()
df["shipping"] = df["shipping"].replace(["", "N/A"], pd.NA)
df["shipping"] = df["shipping"].fillna("Shipping info unavailable")


# Convert prices to numeric

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

# Compute discount percentage

df["discount_percentage"] = (
    ((df["original_price"] - df["price"]) / df["original_price"]) * 100
).round(2)

# Handle divide-by-zero or missing values
df["discount_percentage"] = df["discount_percentage"].fillna(0)


# Save cleaned dataset

df.to_csv("cleaned_ebay_deals.csv", index=False)
print("Cleaned data saved to cleaned_ebay_deals.csv")
