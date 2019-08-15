import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data! \n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Would you like to see data for Chicago, New York City, or Washington? \n")).strip().lower()
            if city in CITY_DATA:
                break
            else:
                print("\nSorry, that is not an available city.\n")
        except ValueError:
            print("\nSorry, that is not an available city.\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\nWhich month do you want to filter by (i.e. January, February, etc)? Type "all" for no month filter \n')).strip().lower()
            if month in months:
                break
            else:
                print("\nSorry, please choose a valid month")
        except ValueError:
            print("\nSorry, that is not a valid month.")

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\nWhich day do you want to filter by (i.e. Monday, Tuesday, etc)? Type "all" for no day filter \n')).strip().lower()
            if day in days:
                break
            else:
                print("\nSorry, please choose a valid day")
        except ValueError:
            print("\nSorry, that is not a valid day.")

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

        # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    mc_month = df['month'].mode()[0]
    print("Most common month: ", mc_month)

# TO DO: display the most common day of week
    mc_weekday = df['day_of_week'].mode()[0]
    print("Most common weekday: ", mc_weekday)

# TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mc_hour = df['hour'].mode()[0]
    print("Most common start hour: ", mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mc_start_station = df['Start Station'].mode()[0]
    print("Most common start station: ", mc_start_station)

    # TO DO: display most commonly used end station
    mc_end_station = df['End Station'].mode()[0]
    print("Most common end station: ", mc_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' -> ')
    mc_combo = df['Trip'].mode()[0]
    print("Most frequent station combination: ", mc_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types: ", user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'].fillna('Unknown', inplace=True)
        gender_count = df['Gender'].value_counts()
        print("Count of gender: ", gender_count)

    else:
        print('Gender information not available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()
        print('Earliest birth year: ', earliest)
        print('Most recent birth year: ', recent)
        print('Most common birth year: ', common)

    else:
        print('Birth year information not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    rows = 0
    while True:
        display_rows = input('\nWould you like to see individual trip data? Enter yes or no.\n')
        if display_rows.lower() == 'yes':
            print(df.iloc[rows:rows + 5])
            rows += 5

        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
