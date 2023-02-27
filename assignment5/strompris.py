#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetches one day of data for one location from hvakosterstrommen.no API.

    arguments:
        date (datetime object): a given date, defaults to todays date if input is None
        location (str): area code

    return:
        df (dataframe): DataFrame showing the prices of electricity every hour
    """
    if date is None:
        date = datetime.date.today()

    date = date.strftime('%Y/%m-%d') #Changes formatting of date
    date2 = "2022/10-02"
    assert date >= date2, "Given date is before 2022/10-02"
    
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date}_{location}.json"
    r = requests.get(url)
    data = r.json()

    d = {'time_start': [], 'NOK_per_kWh': []}
    for dict in data:
        d['time_start'].append(dict['time_start'])
        d['NOK_per_kWh'].append(dict['NOK_per_kWh'])

    df = pd.DataFrame(data=d)
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")
    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetches prices for multiple days and locations into a single DataFrame

     arguments:
        end_date (datetime object): a given date, defaults to todays date if input is None
        days (int): how many days to fetch data for
        locations (tuple): tuple of area codes

    return:
        df (dataframe): DataFrame showing the prices of electricity every hour for 
                        a certain number of days in the given locations
    """
    if end_date is None:
        end_date = datetime.date.today()

    d = {'location': [], 'location_code': [], 'time_start': [], 'NOK_per_kWh': []}

    for loc in locations:
        for i in range(days):
            date = end_date - datetime.timedelta(days=i)
            date = date.strftime('%Y/%m-%d') #Changes formatting of date
            url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date}_{loc}.json"
            r = requests.get(url)
            data = r.json()

            for dict in data:
                d['time_start'].append(dict['time_start'])
                d['NOK_per_kWh'].append(dict['NOK_per_kWh'])
                d['location_code'].append(loc)
                d['location'].append(LOCATION_CODES[loc])

    df = pd.DataFrame(data=d)
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")
    return df

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """

    
    return alt.Chart(df).mark_line().encode(
        x="time_start",
        y="NOK_per_kWh",
        color="location"
    )
    

# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    # return alt.Chart(df).mark_point().encode(
    #     x="time_start",
    #     y="NOK_per_kWh",
    # )

    return alt.Chart(df).mark_line().transform_window(
    daily_avg="NOK_per_kWh"/24,
    frame=[-3, 3],
    ).encode(
        x="time_start",
        y="daily_avg",
        # color="fylke_name",
        # tooltip=[
        #     "fylke_name",
        #     "population",
        #     "per100k",
        #     "cases",
        #     "date",
        # ]

    )


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    #fetch_prices()
    print(df)
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()

    # df_daily = fetch_day_prices()
    # chart_daily = plot_daily_prices(df_daily)
    # chart_daily.show()


if __name__ == "__main__":
    main()
