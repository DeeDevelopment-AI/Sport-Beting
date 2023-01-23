import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

URL = 'https://api.football-data-api.com/league-matches?key=test85g57&season_id=1625'

r = requests.get(URL)

j = r.json()

data = pd.DataFrame.from_dict(j['data'])

st.title("Football Data Analysis")

# Get the unique values of homeID and awayID
home_teams = data["home_name"].unique()
away_teams = data["away_name"].unique()

# Add a dropdown filter for teams
team = st.selectbox("Select team", home_teams.tolist() + away_teams.tolist())

# Show the data filtered by team
data_filtered = data[(data["home_name"] == team) | (data["away_name"] == team)]
st.dataframe(data_filtered)

# Show a summary of the data
st.write("Number of rows: ", data_filtered.shape[0])
st.write("Number of columns: ", data_filtered.shape[1])


# Show a bar chart of the distribution of totalGoalCount

fig = plt.figure()
data_filtered.groupby("totalGoalCount").size().plot(kind="bar")
plt.xlabel("Total Goal Count")
plt.ylabel("Frequency")
plt.title("Distribution of Total Goal Count")
plt.show()

st.pyplot(fig)

# Show a scatter plot of homeGoalCount vs awayGoalCount
data_filtered_home = data[data["home_name"] == team]
grouped = data.groupby(["homeGoalCount", "awayGoalCount"]).agg(count=("homeGoalCount", "count"))
data_filtered_home = data_filtered_home.merge(grouped, on=["homeGoalCount", "awayGoalCount"])
scatter = plt.figure()
plt.scatter(data_filtered_home["homeGoalCount"], data_filtered_home["awayGoalCount"],
s=data_filtered_home["count"]*20)
plt.xlabel("Home Goal Count")
plt.ylabel("Away Goal Count")
plt.title("Scatter plot of Home Goal Count and Away Goal Count")
plt.show()

st.pyplot(scatter)
# Show the correlation matrix
st.write("Correlation matrix: ", data_filtered.corr(numeric_only = True))