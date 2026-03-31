import pandas as pd
import altair as alt

# Load merged data
merged = pd.read_csv('../data/netflix_with_financials.csv')
merged['year_added'] = merged['year_added'].astype(int)

# Calculate average budget per year
yearly_budget = (
    merged.groupby('year_added')
    .agg(avg_budget=('budget_millions', 'mean'), num_titles=('title', 'count'))
    .reset_index()
)

# Create bar chart
chart = alt.Chart(yearly_budget).mark_bar(color='#E50914').encode(
    x=alt.X('year_added:O', title='Year Added to Netflix'),
    y=alt.Y('avg_budget:Q', title='Average Movie Budget ($ Millions)'),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('avg_budget:Q', title='Avg Budget ($M)', format='.1f'),
        alt.Tooltip('num_titles:Q', title='Number of Movies')
    ]
).properties(
    title='Average Budget of Movies Added to Netflix by Year (2016-2021)',
    width=700,
    height=400
)

# Save
chart.save('viz_budget_over_time.html')
print("Saved viz_budget_over_time.html")
