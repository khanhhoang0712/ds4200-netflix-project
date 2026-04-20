import pandas as pd
import altair as alt

# Load merged data
df = pd.read_csv('../data/netflix_with_financials.csv')

# Filter to 2016-2021
df = df[df['year_added'].between(2016, 2021)]
df = df.dropna(subset=['budget_millions'])
df['year_added'] = df['year_added'].astype(int)

# Remove outliers
df = df[(df['budget_millions'] >= 1) & (df['budget_millions'] <= 300)]

# Calculate average budget per year for the line
avg_budget = df.groupby('year_added').agg(
    avg_budget=('budget_millions', 'mean')
).reset_index()

# Boxplot layer
boxplot = alt.Chart(df).mark_boxplot(
    extent='min-max',
    size=40,
    color='#E50914',
    median=alt.MarkConfig(color='white')
).encode(
    x=alt.X('year_added:O', title='Year Added to Netflix', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('budget_millions:Q', title='Movie Budget ($ Millions)', scale=alt.Scale(domain=[0, 300])),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('budget_millions:Q', title='Budget ($M)', format='.1f')
    ]
)

# Average line layer
avg_line = alt.Chart(avg_budget).mark_line(
    color='#FFD700',
    strokeWidth=2,
    point=alt.OverlayMarkDef(color='#FFD700', size=60)
).encode(
    x=alt.X('year_added:O'),
    y=alt.Y('avg_budget:Q'),
    tooltip=[
        alt.Tooltip('year_added:O', title='Year'),
        alt.Tooltip('avg_budget:Q', title='Avg Budget ($M)', format='.1f')
    ]
)

# Layer both together
chart = (boxplot + avg_line).properties(
    title='Distribution of Movie Budgets on Netflix (2016-2021)',
    width=700,
    height=400
)

chart.save('viz_budget_over_time.html')
print("Saved viz_budget_over_time.html")