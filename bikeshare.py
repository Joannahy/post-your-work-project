import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_valid_input(prompt, valid_options):
    """Ask the user for input until it matches one of the valid options."""
    valid_options_lower = [option.lower() for option in valid_options]
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options_lower:
            return user_input
        print('Invalid input. Please choose from: {}.'.format(', '.join(valid_options)))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('-'*40)

    city = get_valid_input(
        'Give the name of the city you are interested in and press enter (Chicago, New York City, Washington):\n',
        list(CITY_DATA.keys())
    )

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = get_valid_input(
        'For what month? For all months type: "all". Enter a month and press enter:\n',
        months
    )

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = get_valid_input(
        'For what day? For all days type: "all". Enter a day and press enter:\n',
        days
    )

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month !='all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]
    
    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
        day = days.index(day.title())
        df = df[df['day_of_week']==day]
    print('Filered data:  \n',df)
    return df


def clean_NaN(df, col_name, val_to_exchange=None):
    """ Checks and cleans the NaNs. It can exchange a value or delete the row with a NaN """
    if df[col_name].isna().sum() > 0:
        if val_to_exchange is not None:
            print('....Exchanging NaNs for: ', col_name)
            df[col_name] = df[col_name].fillna(val_to_exchange)
        else:
            print('...Deleting NaNs for: ', col_name)
            df = df.dropna(subset=[col_name])
        print('\nResults shape after NaN ajusting: ', df.shape)
    else:
        print('\nNo data to adjust\n')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_idx = df['month'].value_counts().idxmax()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[month_idx-1]
    print('The most common month: \n', month)

    # TO DO: display the most common day of week
    day_of_week = df['day_of_week'].value_counts().idxmax()
    days = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
    day = days[day_of_week]
    print('The most common day of week: \n', day)

    # TO DO: display the most common start hour
    hour = (df['Start Time'].dt.hour).value_counts().idxmax()    
    print('The most common start hour: \n', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: \n', start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: \n', end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + "  -  " + df['End Station']
    start_end =     df['start_end'].mode()[0]
    print('Most frequent combination of start station and end station trip: \n', start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_sum = df['Trip Duration'].sum()
    print('Total travel time for chosen period of time: {} seconds'.format(total_sum))
    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time for chosen period of time: {} seconds'.format(round(mean_time,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    users = df['User Type'].value_counts()
    print('User Types:\n', users)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender= df['Gender'].value_counts()
        print('Gerder counts:{}\n'.format(gender))
    else:
        print('Gender data not available!\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print('Birth Year Stats:\n Earliest: {}\n Most Recent: {}\n Common: {}'.format(earliest,recent,common))
    else:
        print('\nBirth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Display 5 rows of raw data at a time upon user request."""
    start_loc = 0
    while True:
        show = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()
        if show == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if start_loc >= len(df):
                print('No more raw data to display.')
                break
        elif show == 'no':
            break
        else:
            print('Invalid input. Please enter yes or no.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df = clean_NaN(df,'Trip Duration')
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
