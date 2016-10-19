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
    ) # [d = 24h]

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

d_t = 62135780134 # Seconds until 1.1.1970
d_t += int(3600 * 24 * 27.5) # Manual correction
SECONDS_EPOCH = d_t

# SECONDS_EPOCH = 62138156134

# Calculate the max number of days during a year
max_days = [ORBITAL_PERIOD[i]/LEN_DAY[i] for i in range(len(LEN_DAY))]
MAX_DAYS = [int(m)+1 for m in max_days]

def seconds_since_1aD():
    '''
        Given a unix timestamp how many seconds have passed since
        1.1 year 1
    '''
    return int(time.time()) + SECONDS_EPOCH


def dates_from_seconds(seconds):
    '''
        Calculates the current date (year, day) for each planet
        based on number seconds since epoch.

        uses ORBITAL_PERIOD & LEN_DAY
    '''
    # Convert to days
    seconds = float(seconds/ (3600 * 24))

    years, days, remainders = [], [], []

    for i, period in enumerate(ORBITAL_PERIOD):
        # Year from orbital period
        year_float = seconds/period
        year = int(year_float)
        remainder = year_float - year

        # Day from rotational period (len day)
        earth_days = remainder * period
        day = int(earth_days/LEN_DAY[i])

        # Start counting at 1
        years.append(year + 1)
        days.append(day + 1)

        # Remainder is a percentage
        remainders.append(int(round(100*remainder)))

    return years, days, MAX_DAYS, remainders


def get_planet_dates():
    d_t = seconds_since_1aD()
    return dates_from_seconds(d_t)


if __name__ == '__main__':
    year, day, max_day, year_progress = get_planet_dates()
    print year
    print day
    print year_progress