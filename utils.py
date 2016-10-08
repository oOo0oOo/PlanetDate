import time

PLANETS = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto')

# Mean solar day
LEN_DAY = (175.9421,
    116.7490,
    1.002737909350795,
    1.0274907,
    0.41225, # Jupiter, Inferred rot. period  =  9.894 h
    0.442083333, # Saturn: 10.61 h
    0.714166667, # Uranus: 17.14 h
    0.695833333, # Neptune: 16.7 h
    6.387230 # Pluto: wiki
    ) # [d]

# Sidereal orbital period
ORBITAL_PERIOD = (87.969257,
    224.70079922,
    365.256363004,
    686.98,
    4332.820,
    10755.698,
    30687.153,
    60190.029,
    91162.49913 # Pluto: 249.58932 yr * 365.25 days in julian year ?
    ) # [d]

# d_t = 62135780134 # Seconds until 1.1.1970
# d_t += int(3600 * 24 * 27.5) # Manual correction

SECONDS_EPOCH = 62138156134


def seconds_since_1aD():
    '''
        Given a unix timestamp how many seconds have passed since
        1.1 year 1
    '''
    return int(time.time()) + SECONDS_EPOCH


def hours_to_time(hours):
    sec = (hours * 3600) - 62135780134
    sec -= int(365.256363004 * 24 * 3600)
    return sec


def dates_from_seconds_numpy(seconds):
    '''
        Calculates the current date (year, day) for each planet
        based on number of revolutions and rotations since 1 AD.

        Uses data from: http://ssd.jpl.nasa.gov/horizons.cgi, queried 4.10.16
        Precision of len_day values is not always the actual precision of the measurement

        Returns a bad linear approximation...
    '''
    d_t = np.repeat(seconds, LEN_DAY.shape[0])

    remainder, year = np.modf(d_t/ORBITAL_PERIOD)
    earth_days = remainder * ORBITAL_PERIOD
    remainder2, day = np.modf(earth_days / LEN_DAY)

    year = (year + 1).astype('uint') # Normal humans start counting at 1
    day = (day + 1).astype('uint')

    # Remainders indicate percentage of progress along the current year / day
    remainder = np.round(100 * remainder).astype('uint')
    remainder2 = np.round(100* remainder2).astype('uint')

    return list(year), list(day), list(remainder)



def dates_from_seconds(seconds):
    '''
        A non-numpy version
    '''
    seconds = float(seconds)

    years, days, remainders = [], [], []

    for i, period in enumerate(ORBITAL_PERIOD):
        year_float = seconds/period
        year = int(year_float)
        remainder = year_float - year

        earth_days = remainder * period
        day = int(earth_days/LEN_DAY[i])

        # Start counting at 1
        years.append(year + 1)
        days.append(day + 1)

        # Remainder is a percentage
        remainders.append(int(round(100*remainder)))

    return years, days, remainders


def get_planet_dates():
    d_t = seconds_since_1aD()
    d_t /= (3600 * 24)
    return dates_from_seconds(d_t)


if __name__ == '__main__':
    year, day, year_progress = get_planet_dates()
    print year
    print day
    print year_progress