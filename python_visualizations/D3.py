import pandas as pd

df = pd.read_csv("data/netflix_cleaned.csv")

df = df.dropna(subset=["country", "type"])

df["country"] = df["country"].str.split(",")
df = df.explode("country")

df["country"] = df["country"].str.strip()

# Save full dataset for D3 filtering
df[["country", "type"]].to_csv("data/netflix_by_country_type.csv", index=False)

print("Saved netflix_by_country_type.csv")