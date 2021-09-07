import time
import calendar
import pandas as pd
import numpy as np

#Work done by Ricardo Soto for Udacity nanodegree

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
    print('\nIf you want to exit just input "exit" at any time\n')

    #Ask the user for information related to city, the loop only accept cities in actual data base
    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input("\nPlease enter the city you want to know (hint: we operate in Chicago, New York City and Washington): \n").lower()
        if city in cities: #Ask if inout is in allowed group of data, if correct finish the check loop.
            break
        elif city == "exit": #finish query if user wants to exit
            print("See you next time!!")
            print("closing...")
            exit()
        else:
            print('We only have information from chicago, new york city and washington =), please try again')

    # get user input for month (all, january, february, ... , june), data setted to lower case to avoid input errors
    months = ('january','february', 'march', 'april', 'may', 'june', 'all')
    while True:
        month = input("\nPlease enter the month you want to know (full name required i.e. january... june or 'all' for no filter): \n").lower()
        if month in months: #Ask if inout is in allowed group of data, if correct finish the check loop.
            break
        elif city == "exit": #finish query if user wants to exit
            print("See you next time!!")
            print("closing...")
            exit()
        else:
            print('Only have information for english named months =), please try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('monday','tuesday','wednesday','thursday', 'friday', 'saturday', 'sunday','all')
    while True:
        day = input("\nPlease enter the day you want to know (monday... sunday or 'all' for complete week): \n").lower()
        if day in days: #Ask if inout is in allowed group of data, if correct finish the check loop.
            break
        elif city == "exit": #finish query if user wants to exit
            print("See you next time!!")
            print("closing...")
            exit()
        else:
            print('we only undestand complete sentence of days like "monday" =), please try again')

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

    #get data from selected City

    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    #creates a condition where the selected day is transformed into integer and match transformation of new column.
    if day != 'all':

        days = ['monday','tuesday','wednesday','thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month tranformed from integer
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()
    most_common_month = int(most_common_month)
    most_common_month = calendar.month_name[most_common_month]
    print('Most common month is: ', most_common_month)

    # display the most common day of week tranformed from integer
    df['day_of_week'] = df['Start Time'].dt.weekday
    most_common_day = df['day_of_week'].mode()
    most_common_day = int(most_common_day)
    most_common_day = calendar.day_name[most_common_day]
    print('Most common day is: ', most_common_day)

    # display the most common start hour transformed to integer
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()
    print('Most common hour is: ', int(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_se = df['Start Station'].mode()[0]
    print('Most common start station: ', most_common_se)


    # display most commonly used end station
    most_common_ee = df['End Station'].mode()[0]
    print('Most common end station: ',most_common_ee)

    # display most frequent combination of start station and end station trip
    df['combination'] = (df['Start Station'] + ' with ' + df['End Station'])
    most_common_combination = df['combination'].mode()[0]
    print('Most common combination: ',most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('Total travel time was: ', travel_time)

    # display mean travel time
    travel_average = df['Trip Duration'].mean()
    print('Total average time was: ', travel_average)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type:')
    print(df['User Type'].value_counts())
    #excludes washington due doees not have information related to birthdays
    if city != 'washington':
        # Display counts of gender
        print('Users gender: ')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth, generating auxiliar variable
        most_recent = df['Birth Year'].max()
        earliest = df['Birth Year'].min()
        most_com_year = df['Birth Year'].mode()[0]
        print('User birhtday:')
        print('Earliest year of birthday is: ', earliest)
        print('Most recent year of birthday is: ', most_recent)
        print('Most common year of birthday is: ', most_com_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#creates extra function to iterate raw data view
def ask_fordata(df):
    """Thanks for asking our data base"""
    number = 0
    while True:
        #loop for ask information every 5 lines con with 1 keyword, reiterates if yes
        user_input_access = input('\nWould you like to see raw data? (y or n)\n').lower()
        if user_input_access == 'y':
            number = number + 1
            print(df.iloc[(number-1)*5:number*5]) #formula to iterate 5 raws every time
            continue
        elif user_input_access == 'n':
            break
        elif user_input_access == 'exit':
                print("See you next time!!")
                print("closing...")
                exit()
        else:
            print('Please just input "y" for yes or "n" for no')

#main function to call others
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        ask_fordata(df)

        restart = input('\nWould you like to restart? Enter y "yes" or n "no".\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
