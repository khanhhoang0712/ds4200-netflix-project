import pandas as pd

# Load data
data = pd.read_csv('data/netflix_titles_2021.csv')

# Clean
data = data.drop_duplicates()
data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')
data['year_added'] = data['date_added'].dt.year
data['primary_country'] = data['country'].str.split(',').str[0].str.strip()

def parse_duration(duration_str):
    if pd.isna(duration_str):
        return None
    try:
        return int(str(duration_str).split()[0])
    except:
        return None

data['duration_value'] = data['duration'].apply(parse_duration)
data = data.dropna(subset=['type', 'title'])

# Save
data.to_csv('data/netflix_cleaned.csv', index=False)