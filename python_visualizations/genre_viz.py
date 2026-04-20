import pandas as pd
import altair as alt

# Load data
data = pd.read_csv('../data/netflix_cleaned.csv')

# Filter to 2016-2021
data = data.dropna(subset=['year_added'])
data['year_added'] = data['year_added'].astype(int)
data = data[data['year_added'].between(2016, 2021)]

# Split genres
data['genre'] = data['listed_in'].str.split(', ')
data = data.explode('genre')

# Keep top 8 genres overall
top_genres = (
    data.groupby('genre')
    .size()
    .reset_index(name='total')
    .sort_values('total', ascending=False)
    .head(8)['genre']
    .tolist()
)

data = data[data['genre'].isin(top_genres)]

# Count by year and genre
genre_counts = (
    data.groupby(['year_added', 'genre'])
    .size()
    .reset_index(name='count')
)

# Calculate rank per year
genre_counts['rank'] = (
    genre_counts.groupby('year_added')['count']
    .rank(ascending=False, method='first')
    .astype(int)
)

# Selection
selection = alt.selection_point(fields=['genre'], bind='legend')

# Lines
lines = alt.Chart(genre_counts).mark_line(strokeWidth=3).encode(
    x=alt.X('year_added:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('rank:O', title='Rank', scale=alt.Scale(domain=list(range(1, 9)))),
    color=alt.Color('genre:N', title='Genre', scale=alt.Scale(scheme='tableau10')),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('genre:N', title='Genre'),
        alt.Tooltip('rank:O', title='Rank'),
        alt.Tooltip('count:Q', title='Number of Titles')
    ]
).add_params(selection)

# Points
points = alt.Chart(genre_counts).mark_circle(size=100).encode(
    x=alt.X('year_added:O'),
    y=alt.Y('rank:O'),
    color=alt.Color('genre:N', scale=alt.Scale(scheme='tableau10')),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('genre:N', title='Genre'),
        alt.Tooltip('rank:O', title='Rank'),
        alt.Tooltip('count:Q', title='Number of Titles')
    ]
).add_params(selection)

chart = (lines + points).properties(
    title='Netflix Genre Rankings Over Time (2016-2021)',
    width=700,
    height=400
)

chart.save('genre_viz.html')
print("Saved genre_viz.html")