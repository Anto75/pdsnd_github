#this project made by Antonio 2021

import time
import statistics
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
from statistics import mode, StatisticsError

# dictionary of the cities files

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# dictionary for months , days and hours

MONTH_DATA = { 'all': "",'january': 1,'february': 2,'march': 3,'april': 4,'may': 5,'june': 6}
DAY_DATA = { 'all': "",'monday': 0,'tuesday': 1,'wednesday': 2,'thursday': 3,'friday': 4,'saturday': 5,'sunday': 6}
HOUR_DATA = { 'all': "",1:'1:00 AM',2:'2:00 AM',3:'3:00 AM',4:'4:00 AM',5:'5:00 AM',6:'6:00 AM',7:'7:00 AM',8:'8:00 AM',9:'9:00 AM',10:'10:00 AM',11:'11:00 AM',12:'12:00 PM',13:'1:00 PM',14:'2:00 PM',15:'3:00 PM',16:'4:00 PM',17:'5:00 PM',18:'6:00 PM',19:'7:00 PM',20:'8:00 PM',21:'9:00 PM',22:'10:00 PM',23:'11:00 PM',24:'12:00 AM'}

city_list = list(CITY_DATA.keys())
month_list = list(MONTH_DATA.keys())
day_list = list(DAY_DATA.keys())

def convert(seconds):

    # this function converts time units

        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        year, day = divmod(day, 365.25)

        if day == 0 and hour == 0:
            return "%02d minute(s) and %02d second(s)" % (min, sec)
        elif day == 0:
            return "%d hour(s) %02d minute(s) and %02d second(s)" % (hour, min, sec)
        elif year == 0:
            return "%d day(s) %d hours(s) %02d minute(s) and %02d second(s)" % (day, hour, min, sec)
        else:
            return "%d year(s) %d day(s) %d hours(s) %02d minute(s) and %02d second(s)" % (year, day, hour, min, sec)

# this function takes the inputs from the user

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('US bikeshare data.')

    # the user enters the name of the city.

    city = input('Enter the city: (' + city_list[0].title() + ', ' + city_list[1].title() + ', or ' + city_list[2].title() + ') ').lower()
    while city not in city_list:
                city = input("Please enter a valid city name: ").lower()

    # the user enters the month for the analysis.

    month = input('Enter the month: (' + month_list[1].title() + ' through ' + month_list[-1].title() + ' or All) ').lower()
    while month not in month_list:
                month = input("Please enter a valid month: ").lower()

    # the user enters the day of week.

    day = input('Enter the day: (All, Monday, Tuesday, ... Sunday) ').lower()
    while day not in day_list:
                day = input("Please enter a valid day: ").lower()

    return city, month, day


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nLoading data...\n')
    start_time = time.time()
    filename = CITY_DATA.get(city, "")
    df = pd.read_csv(filename)

    # Add columns to dataframe

    df = df.dropna(subset=['Start Station', 'End Station'])
    df['Start_and_End'] = df[['Start Station', 'End Station']].apply(lambda x: ' and '.join(x), axis=1)
    df['Month_ID'] = pd.DatetimeIndex(df['Start Time']).month
    df['Day_of_Week_ID'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    df['Hour_of_Day_ID'] = pd.DatetimeIndex(df['Start Time']).hour
    df['Trip_Duration'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.total_seconds()

    # Filter the data with get_filters() function

    if month == 'all' and day != 'all':
        is_day =  df['Day_of_Week_ID']==DAY_DATA.get(day, "")
        df = df[is_day]

    elif day == 'all' and month != 'all':
        is_month =  df['Month_ID']==MONTH_DATA.get(month, "")
        df = df[is_month]

    elif month != 'all' and day != 'all':
        is_month =  df['Month_ID']==MONTH_DATA.get(month, "")
        month_filter = df[is_month]
        is_month_and_day =  month_filter['Day_of_Week_ID']==DAY_DATA.get(day, "")
        df = month_filter[is_month_and_day]

    print("You loaded the file: " + str(filename))

    print('-'*10)

    return df

def time_stats(df):

    start_time = time.time()

    try:
        print('The most common month is ' + list(MONTH_DATA.keys())[list(MONTH_DATA.values()).index((statistics.mode(df['Month_ID'])))].title())
    except StatisticsError:
        print ("Most common month not found. Please select new parameters. :)")
    try:
        print('The most common day of the week is ' + list(DAY_DATA.keys())[list(DAY_DATA.values()).index((statistics.mode(df['Day_of_Week_ID'])))].title())
    except StatisticsError:
        print ("Most common day of the week not found. Please select new parameters. :)")
    try:
        print('The most common hour of the day is ' + list(HOUR_DATA.values())[list(HOUR_DATA.keys()).index((statistics.mode(df['Hour_of_Day_ID'])))].upper())
    except StatisticsError:
        print ("Most common hour of the day not found. Please select new parameters. :)")


    print('-'*10)

def station_stats(df):

    print('\nFinding The Most Common Bike Stations...\n')
    start_time = time.time()

    try:
        print('The most common start station is ' + (statistics.mode(df['Start Station'])).title())
    except StatisticsError:
        print ("Most common start station not found. Please select new parameters. :)")
    try:
        print('The most common end station is ' + (statistics.mode(df['End Station'])).title())
    except StatisticsError:
        print ("Most common end station not found. Please select new parameters. :)")
    try:
        print('The most common combination of start and end station is ' + (statistics.mode(df['Start_and_End'])).title())
    except StatisticsError:
        print ("Most common start and end station combo not found. Please select new parameters. :)")


    print('-'*10)

def trip_duration_stats(df):

    print('\nCalculating trip durations...\n')
    start_time = time.time()

    try:
        print('The average trip duration was ' + convert(statistics.mean(df['Trip_Duration'])))
    except StatisticsError:
        print ("Not able to calculate average trip duration. Please select new parameters. :)")

    print('The total duration of all the trips was ' + convert(sum(df['Trip_Duration'])))


    print('-'*10)

def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    pd.set_option('precision', 0)

    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        user_types = df['User Type'].value_counts().map('{:,}'.format).to_string()
        gender = df['Gender'].value_counts().map('{:,}'.format).to_string()
        most_common_by = df['Birth Year'].value_counts().head(3).map('{:,.0f}'.format).to_string()
        print("Here is the breakdown of user types:", user_types, "\n", sep="\n")
        print("Here is the breakdown of gender:", gender, "\n", sep="\n")
        print("Here are the three most common birth years and counts: \n" + most_common_by + "\n")
        print("The earliest birth year is " + str(format(min(df['Birth Year']), '.0f')) +".", "The most recent birth year is " + str(format(max(df['Birth Year']), '.0f')) +".", sep="\n")

    else:
        user_types = df['User Type'].value_counts().map('{:,}'.format).to_string()
        print("User types:", user_types, "\n", sep="\n")

    print('-'*10)

def display_data(df):

    raw_data = input('\nWould you like to see raw data? (Enter yes or no) \n')
    i = 0

    while raw_data == 'yes':

        if raw_data.lower() == 'yes':
            print(df.head(i + 5))
        raw_data = input('\nWould you like to see 5 more rows of raw data? (Enter yes or no) \n')
        if raw_data.lower() == 'no':
            break
        else: i = i +5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
