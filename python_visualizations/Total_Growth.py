import pandas as pd
import altair as alt

# Load cleaned data
data = pd.read_csv('data/netflix_cleaned.csv')

# Drop missing years
data = data.dropna(subset=['year_added'])
data['year_added'] = data['year_added'].astype(int)

growth = (
    data.groupby('year_added')
        .size()
        .reset_index(name='total_titles')
)
# line chart
chart = alt.Chart(growth).mark_line(point=True).encode(
    x=alt.X('year_added:O', title='Year Added'),
    y=alt.Y('total_titles:Q', title='Number of Titles'),
    tooltip=['year_added', 'total_titles']
).properties(
    title='Total Netflix Content Growth Over Time',
    width=700,
    height=400
)

# Save 
chart.save("python_visualizations/total_growth.html")
print("Saved total_growth.html")
