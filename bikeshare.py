import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ', '.join(c.title() for c in CITY_DATA.keys())
    city_prompt = 'Please enter the name of one of the folowing cities: ' + city_list + '>> '
    city = input(city_prompt).lower()

    while city not in CITY_DATA:
        city_prompt = 'Your entry was not one of the folowing cities: ' + city_list + '. Please try again. >> '
        city = input(city_prompt).lower()        

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_month_numbers = ['1', '2', '3', '4', '5', '6']
    valid_month_names = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_month_abbreviations = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

    input_month = input('Please enter a month from January to June. Enter "all" if you would like to include data from all months. >> ').lower().strip('.')

    while input_month != 'all' \
        and input_month not in valid_month_numbers \
        and input_month not in valid_month_names \
        and input_month not in valid_month_abbreviations:
            input_month = input('The month you entered is not valid. Please pick a month from January through June or type "All". >> ').lower().strip('.')

    if len(input_month) == 1:
        month = valid_month_names[valid_month_numbers.index(input_month)]
    elif len(input_month) == 3 and input_month != 'all':
        month = valid_month_names[valid_month_abbreviations.index(input_month)]
    else:
        month = input_month

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    valid_day_abbreviations = ['mon', 'tues', 'wed', 'thur', 'fri', 'sat', 'sun']

    input_day = input('Please enter a weekday such as "Monday". >> ').lower().strip('.')

    while input_day != 'all' \
        and input_day not in valid_days \
        and input_day not in valid_day_abbreviations:
            input_day = input('The day you entered was not valid. Please enter a weekday such as "Monday". >> ').lower().strip('.')

    if len(input_day) == 3 and input_day != 'all':
        day = valid_days[valid_day_abbreviations.index(input_day)]
    else:
        day = input_day
    
    print('-'*40)
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
    #Import the CSV file into the dataframe.
    df = pd.read_csv(CITY_DATA[city])
    
    #Convert the start time to a datetime object.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #Add month column.
    df['month'] = df['Start Time'].dt.month
    
    #Add day column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #Add Start Hour column.
    df['hour'] = df['Start Time'].dt.hour
    
    #Add Route column.
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_index = df['month'].mode()
    count = len(popular_month_index)
    #popular_month_name = month_names[popular_month_index]
    
    if count == 1:
        print('The most common month is ' + month_names[popular_month_index[0]-1])
    else:
        popular_months = []
        for i in popular_month_index:
            popular_months.append(month_names[i -  1])
        print('The most common months are ' + ', '.join(popular_months))
        
    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()
    count = popular_day_of_week.size
    
    if count == 1:
        print('The most common day is ' + popular_day_of_week[0])
    else:
        print('The most common days are ' + ', '.join(popular_day_of_week.to_list()))
        
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()
    count = popular_hour.size
    
    if count == 1:
        print('The most common start hour is ' + str(popular_hour[0]))
    else:
        print('The most common start hours are ' + ''.join(str(popular_hour.to_list())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()
    count = popular_start_station.size

    if count == 1:
        print('The most commonly used start station is ' + popular_start_station[0])
    else:
        print('The most commonly used start stations are: ' + ', '.join(popular_start_station.to_list()))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()
    count = popular_end_station.size

    if count == 1:
        print('The most commonly used end station is ' + popular_end_station[0])
    else:
        print('The most commonly used end stations are ' + ', '.join(popular_end_station.to_list()))

    # TO DO: display most frequent combination of start station and end station trip
    popular_route = df['route'].mode()
    count = popular_route.size
    
    if count == 1:
        print('The most commonly used route is ' + popular_route[0])
    else:
        print('The most commonly used routes are ' + ', '.join(popular_route.to_list()))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_seconds = df['Trip Duration'].sum()
    total_minutes = total_seconds // 60
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes - (total_hours * 60)
    remaining_seconds = total_seconds - (total_minutes * 60)
    
    print('The total time is {0:.2f} hours, {1:.2f} minutes and {2:.2f} seconds.'.format(total_hours, remaining_minutes, remaining_seconds))
    
    # TO DO: display mean travel time
    average_seconds = df['Trip Duration'].mean()
    average_minutes = average_seconds // 60
    average_hours = average_minutes // 60
    average_remaining_minutes = average_minutes - (average_hours * 60)
    average_remaining_seconds = average_seconds - (average_minutes * 60)

    print('The average trip takes {0:.2f} hours, {1:.2f} minutes and {2:.2f} seconds.'.format(average_hours, average_remaining_minutes, average_remaining_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df.groupby(['User Type'])['User Type'].count()
    print('Here are the counts of the user types:')
    print(user_type_counts)
    print('\n')
    
    # TO DO: Display counts of gender
    if 'Gender' in df:
        df['Gender'] = df['Gender'].fillna('Unknown')
        user_gender_counts = df.groupby(['Gender'])['Gender'].count()
        print('Here are the counts of the user genders:')
        print(user_gender_counts)
        print('\n')
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        popular_birth_year = df['Birth Year'].mode()
        count = popular_birth_year.size
    
        print('The minimum year is ' + str(min_birth_year))
        print('The maximum year is ' + str(max_birth_year))
    
        if count == 1:
            print('The most common birth year is ' + str(int(popular_birth_year[0])))
        else:
            print('The most common birth years are ' + ', '.join(str(popular_birth_year.to_list())))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():

# -*- coding: utf-8 -*-
""" This main module prompts the end user for selections, loads data from a CSV file and runs a variety of functions to produce output.
"""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
