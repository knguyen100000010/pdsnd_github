import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = {'all': 123, 'january': 1, 'february': 2,
          'march': 3, 'april': 4, 'may': 5, 'june': 6}

DAYS = {'all': 123, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ''
    while not city.lower() in CITY_DATA:
        city = input("Enter a city (chicago, new york city, or washington):")

    month = ''
    while not month.lower() in MONTHS:
        month = input("Enter month (all, january, february, ... , june):")

    day = ''
    while not day.lower() in DAYS:
        day = input("Enter day (all, monday, tuesday, ... sunday):")

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

    if city.lower() == 'new york city':
        city = 'new_york_city'

    df = pd.read_csv(city.lower() + '.csv')

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month.lower() == 'all' and day.lower() == 'all':
        return df

    if month.lower() == 'all':
        newdf = df.loc[df["Start Time"].dt.weekday == DAYS[day.lower()]]
        return newdf

    if day.lower() == 'all':
        newdf = df.loc[df["Start Time"].dt.month == MONTHS[month.lower()]]
        return newdf

    newdf = df.loc[(df["Start Time"].dt.weekday == DAYS[day.lower()]) & (
        df["Start Time"].dt.month == MONTHS[month.lower()])]

    return newdf


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df_hour = df.copy()
    df_day = df.copy()
    df_month = df.copy()

    df_hour['Hour'] = df_hour['Start Time'].dt.hour
    df_hour = df_hour.groupby(['Hour']).size().reset_index(name='counts')
    print('The most common hour is: ' +
          str(df_hour.iloc[df_hour["counts"].idxmax()]['Hour']))

    df_day['Day'] = df_day['Start Time'].dt.weekday_name
    df_day = df_day.groupby(['Day']).size().reset_index(name='counts')
    print('The most common day is: ' +
          str(df_day.iloc[df_day["counts"].idxmax()]['Day']))

    df_month['Month'] = df_month['Start Time'].dt.month_name()
    df_month = df_month.groupby(['Month']).size().reset_index(name='counts')
    print('The most common month is: ' +
          str(df_month.iloc[df_month["counts"].idxmax()]['Month']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df_start = df.copy()
    df_end = df.copy()
    df_combine = df.copy()

    df_start = df_start.groupby(
        ['Start Station']).size().reset_index(name='counts')
    print('The most common start station is: ' +
          str(df_start.iloc[df_start["counts"].idxmax()]['Start Station']))

    df_end = df_end.groupby(['End Station']).size().reset_index(name='counts')
    print('The most common end station is: ' +
          str(df_end.iloc[df_end["counts"].idxmax()]['End Station']))

    df_combine = df_combine.groupby(
        ['Start Station', 'End Station']).size().reset_index(name='counts')
    max_index = df_combine["counts"].idxmax()
    print('The most common combined start-end station is: ' +
          str(df_combine.iloc[max_index]['Start Station']) + ' ---> ' + str(df_combine.iloc[max_index]['End Station']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    ty_res = time.gmtime(df['Trip Duration'].sum())
    print('Total trip duration in is : ' + time.strftime("%H:%M:%S", ty_res))

    ty_res = time.gmtime(df['Trip Duration'].mean())
    print('Mean trip duration is : ' +
          time.strftime("%H:%M:%S", ty_res) + ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    df_user_type = df.copy()
    df_gender = df.copy()
    df_birth = df.copy()

    df_user_type = df_user_type.groupby(
        ['User Type']).size().reset_index(name='counts')
    print(df_user_type)

    if 'Gender' in df_gender:
        df_gender = df_gender.groupby(
            ['Gender']).size().reset_index(name='counts')
        print(df_gender)

    if 'Birth Year' in df_birth:
        df_birth = df_birth.groupby(
            ['Birth Year']).size().reset_index(name='counts')
        print('The most common birth year is: ' +
              str(int(df_birth.iloc[df_birth["counts"].idxmax()]['Birth Year'])))
        print('The youngest birth year is: ' +
              str(int(df_birth['Birth Year'].max())))
        print('The oldest birth year is: ' +
              str(int(df_birth['Birth Year'].min())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rows(df):
    number_of_rows_per_display = 5
    start_index = 0
    end_index = 0
    while True:
        rows_display = input(
            '\nWould you like to display the next 5 rows of the raw input data? Enter yes or no.\n')
        if rows_display.lower() != 'yes':
            return

        start_index = end_index
        end_index = start_index + number_of_rows_per_display
        if end_index > len(df.index):
            end_index = len(df.index)

        if start_index >= len(df.index):
            print('All rows have been displayed')
            return

        print(df.iloc[start_index:end_index])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
