import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
       Asks user to specify a city, month, and day to analyze.

       Returns:
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
       """

    city = input('Which city that you would like to check: Chicago, New York, or Washington D.C.?\n').lower()
    month, day = 'all', 'all' # this if the user chose 'none' to not apply filters by month or day
    while city not in (CITY_DATA.keys()):
        print('This is invalid city')
        city = input('Which city that you would like to check: Chicago, New York, or Washington D.C.?\n').lower()

    filter_input = input('Would you like to filter the data by month, day, both, or none?\n')
    while filter_input not in ['month', 'day', 'both', 'none']:
        print('This is invalid filter')
        filter_input = input('Would you like to filter the data by month, day, both, or none?\n')

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    if filter_input == 'month' or filter_input == 'both':
        month = input("Which month? Jan, Feb, Mar, Apr, May, or Jun.\n").lower()
        while month not in months:
            print('This is invalid month')
            month = input("Enter one of the following: Jan, Feb, Mar, Apr, May, or Jun.\n").lower()
    # else:
    #     month = 'all'

    if filter_input == 'day' or filter_input == 'both':
        day = input("Which day? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, or Friday.\n").lower()
        while day not in days:
            print('This is invalid day')
            day = input("Enter either: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, or Friday.\n").lower()
    # else:
    #     day = 'all'

    print('Hello! Let\'s explore some US bikeshare data!')
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
    df = pd.read_csv(CITY_DATA[city])
    # To convert the Start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # To extract month from the from the time column
    df['month'] = df['Start Time'].dt.month
    # To extract weekday from the time column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # To extract hour from the time column
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # To display the most common month
    popular_month = df['month'].mode()[0]
    # To display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    # To display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('The most frequent month is: {}'.format(popular_month))
    print('The most frequent day is: {}'.format(popular_day))
    print('The most frequent hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # To display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    # To display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    # To display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    # head positional argument is set to 1 to demonstrate only the most popular combination of stations (one-line)

    print('The most frequent start station is: {}'.format(popular_start_station))
    print('The most frequent end station is: {}'.format(popular_end_station))
    print('The most frequent combination of stations is:\n {}'.format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # To display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    # To display mean travel time
    average_trip_duration = df['Trip Duration'].mean()

    print('The total travel time is: {}'.format(total_trip_duration))
    print('The average travel time is: {}'.format(average_trip_duration))


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_count = df['User Type'].value_counts()
    # To display counts of user types
    print(user_type_count)
    # To display counts of gender
    gender_count = df['Gender'].value_counts()
    # To display earliest, most recent, and most common year of birth
    frequent_birth_year = df['Birth Year'].mode()[0]
    oldest_subscriber = df['Birth Year'].min()
    youngest_subscriber = df['Birth Year'].max()

    if city != 'washington':
        print(gender_count)
        print('The most frequent birth year is: {}'.format(frequent_birth_year))
        print('The oldest user was born in: {}'.format(oldest_subscriber))
        print('The youngest user was born in: {}'.format(youngest_subscriber))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    answer = input('Would you like to show 5 rows of the raw data?\n').lower()
    while True:
        if answer == 'y':
            print(df.sample(n=5))
            answer = input('Would you like to see other 5 rows?\n').lower()
        elif answer == 'n':
            break
        else:
            print("This is invalid input.")
            answer = input("Please choose either 'y' for Yes or 'n' for No \n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
