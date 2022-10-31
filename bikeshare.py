import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Change #1 For Project
    Change #2 For Project

    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please select how you would like to filter the data from the following options')

    """Loop to get users input"""

    while True:
        city_input = input('Please enter either "c" for Chicago, "n" for New York, or "w" for washington: ')
        print('\n')
        month_input = input ('Please enter the first three characters of the month that you wish to filter for E.g. "jan" for January,\nor use "all" to apply no month filter: ')
        print('\n')
        day_input = input ('Please enter the first two characters of the day that you wish to filter for E.g "su" for Sunday,\nor use "all" to apply no day filter: ')
        print('\n')

        city_conv = (str(city_input)).lower()
        month_conv = (str(month_input)).lower()
        day_conv = (str(day_input)).lower()
        """Check that input is in the list of potential inputs"""
        city_allowable = ('c','n','w')
        month_allowable = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','all')
        day_allowable = ('su','mo','tu','we','th','fr','sa','all')

        if (city_conv in city_allowable) and (month_conv in month_allowable) and (day_conv in day_allowable):
            break
        else:
            print('Your filter selections were invalid, please try again with valid inputs \n')
            continue

    c = {"c": "chicago",'n': "new york city","w": "washington"}
    m = {"jan": "january","feb": "february","mar": "march","apr": "april","may": "may","jun": "june","jul": "july","aug": "august","sep": "september","oct": "october","nov": "november","dec": "december","all": "all"}
    d = {"su": "sunday","mo": "monday","tu": "tuesday","we": "wednesday","th": "thursday","fr": "friday","sa": "saturday","su": "sunday","all": "all"}

    global city
    city = c[city_conv]
    month = m[month_conv]
    day = d[day_conv]

    """Inform user of filter selections"""

    print('Your filter selections of City: {} , Month: {}, Day: {} will now be processed below.'.format(city.capitalize(),month.capitalize(),day.capitalize()))

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

    conversion_m = {"january": 1 ,"february": 2 , "march": 3 , "april" : 4 , "may" : 5 , "june" : 6 , "july" : 7 , "august" : 8 , "september" : 9, "october": 10, "november" : 11, "december" : 12, "all" : 0}
    conversion_d = {"monday": 0 ,"tuesday": 1 , "wednesday": 2 , "thursday" : 3 , "friday" : 4 , "saturday" : 5 , "sunday" : 6 , "all" : 7}

    mc = conversion_m[month]
    dc = conversion_d[day]

    city_f = pd.read_csv(CITY_DATA[city])
    city_f['Start Time'] = pd.to_datetime(city_f['Start Time'])

    if mc == 0:
        month_f = city_f
    else:
        month_f = city_f[city_f['Start Time'].dt.month == mc]

    if dc == 7:
        day_f = month_f
    else:
        day_f = month_f[month_f['Start Time'].dt.dayofweek == dc]

    df = day_f

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    conversion_m = {"january": 1 ,"february": 2 , "march": 3 , "april" : 4 , "may" : 5 , "june" : 6 , "july" : 7 , "august" : 8 , "september" : 9, "october": 10, "november" : 11, "december" : 12}

    conversion_d = {"monday": 0 ,"tuesday": 1 , "wednesday": 2 , "thursday" : 3 , "friday" : 4 , "saturday" : 5 , "sunday" : 6}

    month = df.groupby(df['Start Time'].dt.month)['Trip Duration'].count().reset_index(name="count")
    max_month = np.amax(month['count'])
    i = month['count'].idxmax()
    info = month.iloc[i]
    month_id = info['Start Time']
    month_name = (list(conversion_m.keys())[list(conversion_m.values()).index(month_id)]).capitalize()

    print('The most common month in the filtered data is: {}.'.format(month_name))
    print('\n')

    day = df.groupby(df['Start Time'].dt.weekday)['Trip Duration'].count().reset_index(name="count")
    max_day = np.amax(day['count'])
    i = day['count'].idxmax()
    info = day.iloc[i]
    day_id = info['Start Time']
    day_name = (list(conversion_d.keys())[list(conversion_d.values()).index(day_id)]).capitalize()

    print('The most common day in the filtered data is: {}.'.format(day_name))
    print('\n')

    hour = df.groupby(df['Start Time'].dt.hour)['Trip Duration'].count().reset_index(name="count")
    max_hour = np.amax(hour['count'])
    i = hour['count'].idxmax()
    info = hour.iloc[i]
    hour_max = (info['Start Time'])

    print('The most common start hour for the filtered data is: {}:00 (24hr).'.format(hour_max))
    print('\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start = df.groupby(['Start Station'])['Trip Duration'].count().reset_index(name="count")
    max_count = np.amax(start['count'])
    i = start['count'].idxmax()
    info = start.iloc[i]
    station = info['Start Station']

    print('The most commonly used start station is "{}" with {} trips begun here.'.format(station,max_count))
    print('\n')

    start = df.groupby(['End Station'])['Trip Duration'].count().reset_index(name="count")
    max_count = np.amax(start['count'])
    i = start['count'].idxmax()
    info = start.iloc[i]
    station = info['End Station']

    print('The most commonly used end station is "{}" with {} trips ended here.'.format(station,max_count))
    print('\n')

    start = df.groupby(['Start Station','End Station'])['Trip Duration'].count().reset_index(name="count")
    max_count = np.amax(start['count'])
    i = start['count'].idxmax()
    info = start.iloc[i]
    station_a = info['Start Station']
    station_b = info['End Station']

    print('The most commonly used combination of stations is "{}" to "{}" with {} trips between the two.'.format(station_a,station_b,max_count))
    print('\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()
    print('The total travel time for the filtered data is {} minutes.\n'.format(total_travel))

    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time for the filtered data is {} minutes. \n'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    ut = df.groupby(['User Type'])['Trip Duration'].count().reset_index(name="count")
    customer_data = ut[ut['User Type'] == 'Customer']
    subscriber_data = ut[ut['User Type'] == 'Subscriber']
    customer_count = int(customer_data['count'])
    subscriber_count = int(subscriber_data['count'])

    print('The split of user types that used the service in the currently filtered data are Customers: {}, and Subscribers: {}.\n'.format(customer_count,subscriber_count))

    if city == 'washington':
     print('Gender data is not available for the filtered city, calculating the next statistic...\n')
    else:
        gt = df.groupby(['Gender'])['Trip Duration'].count().reset_index(name="count")
        ut = df['Gender'].isna().sum()
        male_data = gt[gt['Gender'] == 'Male']
        female_data = gt[gt['Gender'] == 'Female']
        unknown_count = int(ut)
        male_count = int(male_data['count'])
        female_count = int(female_data['count'])
        print('The split of user genders that used the service in the currently filtered data are Male: {}, Female: {}, and Unknown:{}.\n'.format(male_count,female_count,unknown_count))


    if city == 'washington':
        print('Birth year data is not available for the filtered city, calculating the next statistic...\n')
    else:
        by = df.groupby(['Birth Year'])['Trip Duration'].count().reset_index(name="count")
        ir = int(by['Birth Year'].max())
        ie = int(by['Birth Year'].min())
        mc = by['count'].idxmax()
        info = by.iloc[mc]
        mcby = int(info['Birth Year'])
        print('Of the filtered data; the earliest birth year was: {}, the most recent birth year was: {}, the most common birth year was: {}'.format(ie,ir,mcby))
        print('\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        start = 0
        end = 5
        size = df.shape
        limit = size[0]
        while True:
            raw_data = input('Would you like to see the raw data? Enter yes or no.\n')
            if raw_data.lower() == 'yes' and end + 5 < limit:
                    print(df.iloc[start:end,:])
                    start += 5
                    end += 5
                    continue
            elif raw_data.lower() == 'yes' and end + 5 >= limit:
                print(df.iloc[start:limit,:])
                print('Exiting raw data view, record limit reached')
                break
            else:
                print('Exiting raw data view, view exited')
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
