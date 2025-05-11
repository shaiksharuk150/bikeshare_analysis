import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities_names =['chicago','new york city','washington']              

month_names = ['january', 'february','march','april','may', 'june']
month_values =['all', 'january', 'february','march','april','may', 'june']

day_names = ['monday', 'tuesday','wednesday','thursday','friday', 'saturday','sunday']
day_values =['all', 'monday', 'tuesday','wednesday','thursday','friday', 'saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Which City would you choose from 'chicago', 'new york city', 'washington' ?  \n").lower()
    while city not in CITY_DATA:
        city = input("Error !!! Please choose from city ['chicago', 'new york city', 'washington']  \n").lower()


    # get user input for month (all, january, february, ... , june)
    month =input("Which month would you choose from 'all', 'january', 'february','march','april','may', 'june' ? \n").lower()
    while month not in month_values:
        month = input("Error !!! Please choose month from ['all', 'january', 'february','march','april','may', 'june']  \n").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you choose day from 'all', 'monday', 'tuesday','wednesday','thursday','friday', 'saturday','sunday' ? \n").lower()
    while day not in day_values:
        day = input("Error !!! Please choose from ['all', 'monday', 'tuesday','wednesday','thursday','friday', 'saturday','sunday']  \n").lower()


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
    df['day_of_week'] = df['Start Time'].dt.day_name()


    if month != 'all':
        month = month_names.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = month_names[df['month'].mode()[0]-1]
    count_month = count = df['month'].value_counts()[df['month'].mode()[0]]
    print("The most common month of travel is  '{}' count is '{}'".format(common_month,count_month))


    


    # display the most common day of week

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.day_name()
    common_day = df['day_of_week'].mode()[0]
    count_day = df['day_of_week'].value_counts()[common_day]
    
    print("The most common day of travel is '{}' count is '{}'".format(common_day,count_day))



    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour= df['hour'].mode()[0]
    count_hour = df['hour'].value_counts()[common_hour]
    print("The most common day of travel is '{}' hrs count is '{}'".format(common_hour,count_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    """ used chatgpt to to get this logic of common start and end station"""
    # display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts()[common_start_station]
    print("The most common start station is '{}' count is  {}".format(common_start_station,count_start_station))



    # display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts()[common_end_station]
    print("The most common end station is '{}' count is  {} ".format(common_end_station,count_end_station))


    # display most frequent combination of start station and end station trip
    start_and_end = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    max_count = start_and_end['count'].max()
    common_start_end = start_and_end[start_and_end['count'] == max_count]

    print("\nThe most frequent combination of start station and end station trip : \n")

    for _, row in common_start_end.iterrows():
        print(f"Start Station : {row['Start Station']} End Station : {row['End Station']} appears {row['count']} times")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Travel Duration'] = (df['Start Time'] - df['End Time']).dt.seconds
    total_time = df['Travel Duration'].sum()
    total_travel_hours= total_time // 3600
    total_travel_minutes= (total_time % 3600) // 60
    total_travel_seconds = total_time % 60

    print(f"The total travel time is {total_travel_hours} hrs {total_travel_minutes} mins {total_travel_seconds} secs")
 


    # display mean travel time
    total_mean_time = df['Travel Duration'].mean()
    mean_travel_hours= total_mean_time // 3600
    mean_travel_minutes= (total_mean_time % 3600)  // 60
    mean_travel_seconds = total_mean_time % 60
    print(f"The mean Travel Time is {int(mean_travel_hours)} hrs  {int(mean_travel_minutes)} mins {int(mean_travel_seconds)} secs")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    count_user_types = df.groupby(['User Type'])['User Type'].count()
    print(count_user_types)
    for user_type, count in count_user_types.items() :
        print("The count of {} is : {}".format(user_type,count))

    print("-" * 40)

    # Display counts of gender

    if 'Gender' in df:
        count_gender = df.groupby(['Gender'])['Gender'].count()
        print(count_gender)

        for gender, count in count_gender.items() :
            print("The count of {} is : {}".format(gender,count))
    else:
        print(f"Gender column information is not present in the {city} data")

    print("-" * 40)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print(f"The most earliest birth year is {int(earliest_year)}")
        recent_year = df['Birth Year'].max()
        print(f"The most recent birth year is {int(recent_year)}")
        common_year = df['Birth Year'].mode()[0]
        count_common_year = df['Birth Year'].value_counts()[common_year]
        print(f"The most common birth year is {int(common_year)} count is '{count_common_year}'")
    else:
        print(f"Birth Year column information is not present in the {city} data")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
