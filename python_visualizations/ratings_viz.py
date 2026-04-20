import pandas as pd
import altair as alt

# Load ratings data
data = pd.read_csv('../data/netflix_ratings.csv')
data['year_added'] = data['year_added'].astype(int)

# Set correct order for rating groups
rating_order = ['Kids', 'Older Kids', 'Teen', 'Mature', 'Other']

# Heatmap layer
heatmap = alt.Chart(data).mark_rect().encode(
    x=alt.X('year_added:O', title='Year Added to Netflix', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('rating_group:N', title='Rating Group', sort=rating_order),
    color=alt.Color('percentage:Q',
        title='% of Content',
        scale=alt.Scale(scheme='reds')
    ),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('rating_group:N', title='Rating Group'),
        alt.Tooltip('count:Q', title='Number of Titles'),
        alt.Tooltip('percentage:Q', title='Percentage', format='.1f')
    ]
)

# Text labels layer
text = alt.Chart(data).mark_text(fontSize=12, fontWeight='bold').encode(
    x=alt.X('year_added:O'),
    y=alt.Y('rating_group:N', sort=rating_order),
    text=alt.Text('percentage:Q', format='.1f'),
    color=alt.condition(
        alt.datum.percentage > 25,
        alt.value('white'),
        alt.value('black')
    )
)

# Layer both
chart = (heatmap + text).properties(
    title='Netflix Content Rating Distribution by Year (2016-2021)',
    width=700,
    height=350
)

chart.save('viz_ratings.html')
print("Saved viz_ratings.html")