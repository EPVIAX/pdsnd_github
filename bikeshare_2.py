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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =''
    while city not in ('chicago','new york city','washington'):
        city = input('Ingrese la ciudad que desea analizar (chicago, new york city, washington):')
        city = city.lower()
        #print(city)
        #print(city in ('chicago','new york city','washington'))

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ('january', 'february' , 'march', 'april', 'may', 'june', 'all'):
        month = input('Ingrese el mes que desea analizar (january,february,march,april,may,june) o escriba all: \n')
        month = month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input('Ingrese el dia que desea analizar (monday, tuesday, wednesday, thursday, friday, saturday, sunday) o escriba all:')
        day = day.lower()
        
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['star_hour'] = df['Start Time'].dt.hour

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

    # display the most common month
    common_month = df['month'].mode()[0]
    acc_month = df['month'].value_counts()[common_month]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('El mes más comun es: {}, con: {} veces'.format(months[common_month-1],acc_month))
    
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    acc_day = df['day_of_week'].value_counts()[common_day]
    print('El día de la semana más comun es: {}, con: {} veces'.format(common_day,acc_day))
    
    # display the most common start hour
    common_start_hour = df['star_hour'].mode()[0]
    acc_start_hour = df['star_hour'].value_counts()[common_start_hour]
    print('La hora de inicio más comun es a las: {} horas, con: {} veces'.format(common_start_hour,acc_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    acc_start_station = df['Start Station'].value_counts()[common_start_station]
    print('La estación de inicio más usada es: {}, -> con: {} veces'.format(common_start_station,acc_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    acc_end_station = df['End Station'].value_counts()[common_end_station]
    print('La estación final más usada es: {}, -> con: {} veces'.format(common_end_station,acc_end_station))

    # display most frequent combination of start station and end station trip
    """"
    tempo = pd.DataFrame(df[['Start Station','End Station']])
    tempo1 = tempo.value_counts()
    most_freq_comb_start = tempo1.index[0][0]
    most_freq_comb_end = tempo1.index[0][1]
    acc_freq_comb_station = tempo1[0]
    print('La combinacion estación inicial: {} con la estación final : {} es la mas frecuente -> con: {} veces'.format(most_freq_comb_start, most_freq_comb_end, acc_freq_comb_station))
    """
    grouped = pd.DataFrame(df.groupby(['Start Station','End Station'])['End Station'].count())
    grouped.columns = ['Value_counts']
    most_freq_comb_start = grouped.idxmax()[0][0]   
    most_freq_comb_end = grouped.idxmax()[0][1]   
    acc_freq_comb_station = grouped['Value_counts'].max()   
    print('La combinacion estación inicial: {} con la estación final : {} es la mas frecuente -> con: {} veces'.format(most_freq_comb_start, most_freq_comb_end, acc_freq_comb_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('El tiempo total de viaje es de {} segundos'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('El tiempo promedio de viaje es de {} segundos'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,ciudad):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    city = ciudad
    # Display counts of user types
    print('La cantidad de usuarios por tipo:\n')
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city in ('chicago','new york city'):
        print('\nLa cantidad de usuarios por genero:\n')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city in ('chicago','new york city'):
        print('\nEl año de nacimiento mas antiguo: {}'.format(int(df['Birth Year'].min())))
        print('El año de nacimiento mas reciente: {}'.format(int(df['Birth Year'].max())))
        print('El año de nacimiento mas común: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def ver_datos(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
    print('******** Finish view ********')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        ver_datos(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()