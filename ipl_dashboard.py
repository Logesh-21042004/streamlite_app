import streamlit as st
import pandas as pd
import altair as alt


# IPL Teams and Sample Stats
team_colors = {
    'Chennai Super Kings': '#F9CD05',
    'Delhi Capitals': '#17479E',
    'Gujarat Titans': '#1C2341',
    'Kolkata Knight Riders': '#3A225D',
    'Lucknow Super Giants': '#005FA2',
    'Mumbai Indians': '#004BA0',
    'Punjab Kings': '#D71920',
    'Rajasthan Royals': '#254AA5',
    'Royal Challengers Bangalore': '#DA2128',
    'Sunrisers Hyderabad': '#F26522',
}
data = {
    'Team': [
        'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders',
        'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
        'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
    ],
    'Matches Played': [265, 255, 76, 275, 76, 285, 260, 255, 275, 215],
    'Wins': [148, 117, 45, 137, 38, 158, 116, 121, 127, 97],
    'Losses': [112, 133, 31, 132, 36, 122, 137, 126, 136, 112],
    'Titles': [5, 0, 1, 2, 0, 6, 0, 1, 0, 2]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="IPL Teams Stats Dashboard", layout="wide")
st.title("🏏 IPL Teams Interactive Dashboard")
st.markdown("""
This dashboard provides an interactive and visually appealing overview of all IPL teams and their key statistics.
""")

# Sidebar for team selection
st.sidebar.markdown("## Team Selection")
    # ...existing code...
selected_teams = st.sidebar.multiselect(
    "Select IPL Teams to View Stats:",
    options=df['Team'],
    default=df['Team']
)

filtered_df = df[df['Team'].isin(selected_teams)]


# Show stats table with logos
st.subheader("Team Statistics Table")
st.write(
    filtered_df.to_html(index=False, columns=['Team', 'Matches Played', 'Wins', 'Losses', 'Titles']),
    unsafe_allow_html=True
)

# Bar chart for Wins
st.subheader("Wins by Team")
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('Team', sort='-y'),
    y='Wins',
    color=alt.Color('Team:N', scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())), legend=None),
    tooltip=['Team', 'Wins']
).properties(height=400)
st.altair_chart(bar_chart, use_container_width=True)

# Pie chart for Titles
st.subheader("Distribution of IPL Titles")
pie_data = filtered_df[filtered_df['Titles'] > 0]
pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta=alt.Theta(field="Titles", type="quantitative"),
    color=alt.Color('Team:N', scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())), legend=None),
    tooltip=['Team', 'Titles']
)
st.altair_chart(pie_chart, use_container_width=True)


# Line chart for Matches Played vs Wins
st.subheader("Matches Played vs Wins")
line_chart = alt.Chart(filtered_df).transform_fold(
    ['Matches Played', 'Wins'],
    as_=['Stat', 'Value']
).mark_line(point=True).encode(
    x=alt.X('Team:N', title='Team'),
    y=alt.Y('Value:Q', title='Count'),
    color=alt.Color('Team:N', scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())), legend=None),
    strokeDash=alt.StrokeDash('Stat:N', legend=alt.Legend(title='Stat')),
    tooltip=[alt.Tooltip('Team:N'), alt.Tooltip('Stat:N'), alt.Tooltip('Value:Q')]
)
st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")
