import pandas as pd

# Load cleaned netflix data
data = pd.read_csv('../data/netflix_cleaned.csv')

# Filter to 2016-2021
data = data[data['year_added'].between(2016, 2021)]
data['year_added'] = data['year_added'].astype(int)

# Drop rows with missing rating
data = data.dropna(subset=['rating'])

# Group ratings into categories
def group_rating(rating):
    if rating in ['TV-MA', 'R', 'NC-17']:
        return 'Mature'
    elif rating in ['TV-14', 'PG-13']:
        return 'Teen'
    elif rating in ['PG', 'TV-PG']:
        return 'Older Kids'
    elif rating in ['G', 'TV-G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV']:
        return 'Kids'
    else:
        return 'Other'

data['rating_group'] = data['rating'].apply(group_rating)

# Count by year and rating group
ratings_by_year = data.groupby(['year_added', 'rating_group']).size().reset_index(name='count')
yearly_totals = data.groupby('year_added').size().reset_index(name='total')
ratings_by_year = ratings_by_year.merge(yearly_totals, on='year_added')
ratings_by_year['percentage'] = (ratings_by_year['count'] / ratings_by_year['total']) * 100

# Save
ratings_by_year.to_csv('../data/netflix_ratings.csv', index=False)
print(ratings_by_year.head(10))
print(f"Saved netflix_ratings.csv with {len(ratings_by_year)} rows")