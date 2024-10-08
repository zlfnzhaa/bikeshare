# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kGC3hO0VlTIKggUPQ8CoEQalXjM_h_oF
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

day_df = pd.read_csv('day_data.csv')
hour_df = pd.read_csv('hour_data.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df['weekday'] = day_df['dteday'].dt.day_name()
hour_df['weekday'] = hour_df['dteday'].dt.day_name()
day_df['mnth'] = day_df['dteday'].dt.month_name()
hour_df['mnth'] = hour_df['dteday'].dt.month_name()
day_df['yr'] = day_df['dteday'].dt.year
hour_df['yr'] = hour_df['dteday'].dt.year

day_df['temp'] = day_df['temp'] * 41
hour_df['temp'] = hour_df['temp'] * 41
day_df['atemp'] = day_df['atemp'] * 50
hour_df['atemp'] = hour_df['atemp'] * 50

def find_season(season):
    season_string = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    return season_string.get(season)

day_df['season'] = day_df['season'].apply(find_season)
hour_df['season'] = hour_df['season'].apply(find_season)

grouped_month = day_df.groupby(by=["mnth"])['cnt'].sum().sort_values(ascending=False).reset_index()

st.header('Bike-sharing Data Dashboard')

st.subheader('Total Bike Sharing by Month')

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="mnth", y="cnt", data=grouped_month, palette='Blues_d', ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Total Count")
ax.set_title("Total Bikeshare Users per Month")
st.pyplot(fig)

st.subheader("Bike Sharing Trend Over Time")

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(x="dteday", y="cnt", data=day_df, color='blue', ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Count")
ax.set_title("Bike Sharing Users Over Time")
st.pyplot(fig)

st.subheader("Total Bike Sharing by Hour")

grouped_hour = hour_df.groupby(by="hr")['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="hr", y="cnt", data=grouped_hour, palette='Blues_d', ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Total Count")
ax.set_title("Total Bikeshare Users per Hour")
st.pyplot(fig)

st.subheader('Bike-sharing Summary')

col1, col2 = st.columns(2)

with col1:
    total_bikes = day_df['cnt'].sum()
    st.metric("Total Bikes Rented", value=total_bikes)

with col2:
    avg_temp = day_df['temp'].mean()
    st.metric("Average Temperature (°C)", value=round(avg_temp, 2))

st.subheader("Bike Sharing by Season")

grouped_season = day_df.groupby('season')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=grouped_season, palette='coolwarm', ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Total Count")
ax.set_title("Bike Sharing Across Seasons")
st.pyplot(fig)

st.subheader("Statistics Summary")
st.write("Day Data Statistics:")
st.dataframe(day_df.describe())

st.write("Hour Data Statistics:")
st.dataframe(hour_df.describe())