import pandas as pd
import altair as alt

# Load ratings data
data = pd.read_csv('../data/netflix_ratings.csv')
data['year_added'] = data['year_added'].astype(int)

# Dropdown filter
dropdown = alt.binding_select(options=[None, 'Mature', 'Teen', 'Older Kids', 'Kids', 'Other'], 
                               labels=['All', 'Mature', 'Teen', 'Older Kids', 'Kids', 'Other'],
                               name='Rating Group: ')
selection = alt.selection_point(fields=['rating_group'], bind=dropdown)

# Create chart
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('year_added:O', title='Year Added to Netflix', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('percentage:Q', title='Percentage of Content (%)', scale=alt.Scale(domain=[0, 100])),
    color=alt.Color('rating_group:N', title='Rating Group'),
    xOffset='rating_group:N',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('rating_group:N', title='Rating Group'),
        alt.Tooltip('count:Q', title='Number of Titles'),
        alt.Tooltip('percentage:Q', title='Percentage', format='.1f')
    ]
).add_params(selection).properties(
    title='Netflix Content Rating Distribution by Year (2016-2021)',
    width=700,
    height=400
)

# Save
chart.save('viz_ratings.html')
print("Saved viz_ratings.html")