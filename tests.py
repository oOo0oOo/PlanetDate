from utils import dates_from_seconds, SECONDS_EPOCH

from datetime import date
import random
import time
import itertools

def all_dates():
    '''
        Return seconds, year and day for a range of dates.
        Note: returns only days 2 - 28 of each month
    '''
    years = range(2016,2048)
    months = range(1,13)
    days = range(2,29)

    data = []

    for year, month, day in itertools.product(*[years, months, days]):
        d = date(year, month, day)

        # Calculate the which day of the year it is
        d0 = date(year, 1, 1)
        delta = d - d0

        # Get number of seconds since 1AD
        unixtime = int(time.mktime(d.timetuple()))
        unixtime += SECONDS_EPOCH
        unixtime /= (3600 * 24)

        data.append((unixtime, year, delta.days + 1))

    return data


if __name__ == '__main__':
    data = all_dates()

    # For the moment just testing whether we do not deviate by
    # more than 1 d from the predicted date on planet earth.

    for seconds, year_exp, day_exp in data:
        year, day, re1 = dates_from_seconds(seconds)

        # Check with predicted year and day
        assert year[2] - year_exp == 0
        assert (day[2] - day_exp) < 2