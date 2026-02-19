import pandas as pd
import altair as alt

# Load data
data = pd.read_csv('data/netflix_cleaned.csv')
data_clean = data[data['year_added'].notna()]

# Count by year and type
yearly_counts = data_clean.groupby(['year_added', 'type']).size().reset_index(name='count')
yearly_totals = data_clean.groupby('year_added').size().reset_index(name='total')
yearly_counts = yearly_counts.merge(yearly_totals, on='year_added')
yearly_counts['percentage'] = (yearly_counts['count'] / yearly_counts['total']) * 100

# Create chart
chart = alt.Chart(yearly_counts).mark_bar().encode(
    x=alt.X('year_added:O', title='Year Added to Netflix', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('percentage:Q', title='Percentage of Content (%)', scale=alt.Scale(domain=[0, 100])),
    color=alt.Color('type:N', 
                    title='Content Type',
                    scale=alt.Scale(domain=['Movie', 'TV Show'], range=['#1f77b4', '#ff7f0e'])),
    xOffset='type:N',
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('type:N', title='Type'),
        alt.Tooltip('count:Q', title='Number of Titles'),
        alt.Tooltip('percentage:Q', title='Percentage', format='.1f')
    ]
).properties(
    title='Netflix Content Evolution: Movies vs TV Shows (2008-2021)',
    width=700,
    height=400
)

# Save
chart.save('python_visualizations/viz1_movies_vs_shows.html')
print('Visualization 1 saved')