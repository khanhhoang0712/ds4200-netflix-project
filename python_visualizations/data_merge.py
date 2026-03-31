import pandas as pd

# Load datasets
netflix = pd.read_csv('../data/netflix_cleaned.csv')
movies_meta = pd.read_csv('../data/movies_metadata.csv', low_memory=False)

# Filter Netflix to movies only
netflix_movies = netflix[netflix['type'] == 'Movie'].copy()

# Clean movies_metadata
movies_meta['budget'] = pd.to_numeric(movies_meta['budget'], errors='coerce')
movies_meta['revenue'] = pd.to_numeric(movies_meta['revenue'], errors='coerce')
movies_meta['release_year'] = pd.to_datetime(movies_meta['release_date'], errors='coerce').dt.year

# Remove rows with missing title or zero budget
movies_meta = movies_meta.dropna(subset=['title'])
movies_meta = movies_meta[movies_meta['budget'] > 0]

# Keep only useful columns and remove duplicates
movies_meta = movies_meta[['title', 'release_year', 'budget', 'revenue']].drop_duplicates(subset=['title', 'release_year'])

# Merge on title and release_year
merged = netflix_movies.merge(movies_meta, on=['title', 'release_year'], how='inner')

# Filter to 2016-2021
merged = merged[merged['year_added'].between(2016, 2021)]

# Convert budget to millions
merged['budget_millions'] = merged['budget'] / 1_000_000

# Save merged dataset
merged.to_csv('../data/netflix_with_financials.csv', index=False)
print(f"Saved netflix_with_financials.csv with {len(merged)} rows")