import pandas as pd
import altair as alt

# Load data
data = pd.read_csv('../data/netflix_cleaned.csv')

# Filter to 2016-2021
data = data.dropna(subset=['year_added'])
data['year_added'] = data['year_added'].astype(int)
data_clean = data[data['year_added'].between(2016, 2021)]

# --- Chart 1: Total Growth ---
growth = (
    data_clean.groupby('year_added')
    .size()
    .reset_index(name='total_titles')
)

growth_chart = alt.Chart(growth).mark_line(
    color='#E50914',
    strokeWidth=3,
    point=alt.OverlayMarkDef(color='#E50914', size=60)
).encode(
    x=alt.X('year_added:O', title='Year Added', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('total_titles:Q', title='Number of Titles'),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('total_titles:Q', title='Total Titles')
    ]
).properties(
    title='Total Netflix Content Growth (2016-2021)',
    width=340,
    height=400
)

# --- Chart 2: Movies vs Shows ---
yearly_counts = data_clean.groupby(['year_added', 'type']).size().reset_index(name='count')
yearly_totals = data_clean.groupby('year_added').size().reset_index(name='total')
yearly_counts = yearly_counts.merge(yearly_totals, on='year_added')
yearly_counts['percentage'] = (yearly_counts['count'] / yearly_counts['total']) * 100

selection = alt.selection_point(fields=['type'], bind='legend')

type_chart = alt.Chart(yearly_counts).mark_line(
    strokeWidth=3,
    point=True
).encode(
    x=alt.X('year_added:O', title='Year Added', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('percentage:Q', title='Percentage of Content (%)', scale=alt.Scale(domain=[0, 100])),
    color=alt.Color('type:N',
        title='Content Type',
        scale=alt.Scale(domain=['Movie', 'TV Show'], range=['#E50914', '#831010'])
    ),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('type:N', title='Type'),
        alt.Tooltip('count:Q', title='Number of Titles'),
        alt.Tooltip('percentage:Q', title='Percentage', format='.1f')
    ]
).add_params(selection).properties(
    title='Movies vs TV Shows Over Time (2016-2021)',
    width=340,
    height=400
)

# Combine side by side
combined = (growth_chart | type_chart).properties(
    title='Netflix Content Growth and Type Evolution (2016-2021)'
)

combined.save('viz1_movies_vs_shows.html')
print("Saved viz1_movies_vs_shows.html")