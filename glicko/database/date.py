from datetime import datetime, timedelta

def parse_date(date):
    date = str(date)
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    return string_to_date(date)

def string_to_date(date):
    date = str(date).split("-")

    y = int(date[0])
    m = int(date[1])
    d = int(date[2])

    return datetime(y, m, d).date()

def date_to_string(date):
    y = date.year
    m = date.month
    d = date.day

    if m < 10:
        m = "0" + str(m)
    if d < 10:
        d = "0" + str(d)

    return "-".join([str(y), str(m), str(d)])

def monday(date):
    date = string_to_date(date)
    date = date - timedelta(days=date.weekday())

    return date

def _fill_dates(start_date, end_date, time_delta):
    dates = [start_date]
    date = start_date

    while date < end_date:
        date += time_delta
        dates.append(date)

    return dates

def get_dates(start_year, end_year, time_delta):
    start_date = "{year}-12-31".format(year=start_year - 1)
    start_date = monday(start_date)

    if end_year == 2022:
        limit_date = datetime.today().date()
    else:
        limit_date = monday(f"{end_year + 1}-01-01")

    i = 1

    while start_date + i * time_delta < limit_date:
        i += 1

    end_date = start_date + i * time_delta

    dates = _fill_dates(start_date, end_date, time_delta)

    return dates  