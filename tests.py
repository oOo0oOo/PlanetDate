from utils import dates_from_seconds, SECONDS_EPOCH

from datetime import date
import random
import time
import itertools

def all_dates():
    '''
        Return seconds, year and day for a range of dates.
        Note: returns only days 1 - 28 of each month
    '''
    years = range(2016,2019)
    months = range(1,13)
    days = range(1,29)

    data = []

    for year, month, day in itertools.product(*[years, months, days]):
        d = date(year, month, day)

        # day of the year
        delta = d.timetuple().tm_yday

        # Get number of seconds since 1AD
        unixtime = int(time.mktime(d.timetuple()))
        unixtime += SECONDS_EPOCH

        # Make it noon
        unixtime += 12*3600

        data.append((unixtime, year, delta + 1))


    return data


if __name__ == '__main__':
    data = all_dates()

    # For the moment just testing whether we do not deviate by
    # more than 1 d from the predicted date on planet earth.
    diffs = []
    for seconds, year_exp, day_exp in data:
        year, day, max_day, re1 = dates_from_seconds(seconds)

        # Check with predicted year and day
        assert year[2] - year_exp == 0
        assert abs(day_exp - day[2]) <= 1

        diffs.append(abs(day_exp - day[2]))

    # Check that its mostly correct
    avg_diff = 1.*sum(diffs)/len(diffs)
    assert avg_diff < 0.3

    # import matplotlib.pyplot as plt
    # print 'Avg difference:', avg_diff
    # plt.hist(diffs)
    # plt.show()