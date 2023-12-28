import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
import numpy as np 
from babel.numbers import format_currency
sns.set(style='dark')

# create hourly_df
def create_hourly_df(df):
    hourly_df = bike_data.groupby('hour')['cnt_hour'].mean().sort_values(ascending=False).reset_index()
    return hourly_df

# create weatherly_df
def create_weatherly_df(df):
    weatherly_df = bike_data.groupby('weathersit_day')['cnt_day'].mean().reset_index().sort_values('cnt_day')
    return weatherly_df

# create holiday_df
def create_holiday_df(df):
    holiday_df = bike_data.groupby('holiday_day')['cnt_day'].mean().reset_index().sort_values("cnt_day")
    return holiday_df

# create monthly_df
def create_monthly_df(df):
    monthly_df = bike_data.groupby('month_day')['cnt_day'].mean().reset_index().sort_values("cnt_day")
    return monthly_df

# create seasonal_df
def create_seasonal_df(df):
    seasonal_df = bike_data.groupby(['season_day', 'year_day'])['cnt_day'].mean().reset_index().sort_values(["season_day","year_day"])
    return seasonal_df

# create correlation_df

bike_data = pd.read_csv("bike_data.csv")

bike_data["datetime"] = pd.to_datetime(bike_data["datetime"])

# Create filter
min_date = bike_data["datetime"].min()
max_date = bike_data["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_data[(bike_data["datetime"] >= str(start_date)) & (bike_data["datetime"] <= str(end_date))]

hourly_df = create_hourly_df(main_df)
weatherly_df = create_weatherly_df(main_df)
holiday_df = create_holiday_df(main_df)
monthly_df = create_monthly_df(main_df)
seasonal_df = create_seasonal_df(main_df)

# Dashboard Visualization
st.header('Bike Sharing Performance Dashboard :bike:')

# Daily Rental
st.subheader('Daily Rental')
col1, col2 = st.columns(2)

with col1:
    total_rental_day = main_df.cnt_day.sum()
    st.metric("Total Rental by Day", value=total_rental_day)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["datetime"],
    main_df["cnt_day"],
    marker='o',
    linewidth=2,
    color="blue"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Monthly Bike Rental
st.subheader("Summary of Bike Rental by Month & Season")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x='month_day', y='cnt_day', data=bike_data, hue='year_day', ax=ax)

    ax.set_title("Total of Bike Rental by Month", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x='season_day', y='cnt_day', data=bike_data, hue='year_day', ax=ax)

    ax.set_title("Total of Bike Rental by Season", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Clusters of Bikeshare Rides by Season and Temperature
fig, ax = plt.subplots(figsize=(16, 8))

sns.scatterplot(x='temp_day', y='cnt_day', data=bike_data, hue='season_day', ax=ax)

ax.set_xlabel("Temperature (degC)")
ax.set_ylabel("Total Rides")
ax.set_title("Clusters of Bikeshare Rides by Season and Temperature (2011 - 2012)")

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Average Bike Rental
st.subheader("Summary of Average Bike Rental")
col1, col2 = st.columns(2)

with col1:
    avg_rental_day = main_df.cnt_day.mean()
    st.metric("Average Rental by Day", value=avg_rental_day)

# Summary of Average Bike Rental

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x='holiday_day', y='cnt_day', data=holiday_df, palette='Set2', ax=ax)

    ax.set_title('Average Bike Rental by Day', loc='center', fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticks([0, 1], ['Workingdays', 'Holiday'])
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x='weathersit_day', y='cnt_day', data=weatherly_df, palette='Set2', ax=ax)

    ax.set_title('Average Bike Rental by Weather Condition', loc='center', fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.caption('Copyright (c) Dicoding')
