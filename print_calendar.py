import datetime


SUNDAY = 6
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def min_sunday(date):
    d = date
    while d.weekday() != SUNDAY:
        d -= datetime.timedelta(days=1)
    return d


def print_calendar(events_index, cell_width, cell_height):
    min_date = min(events_index.keys() + [datetime.date.today()])
    max_date = max(events_index.keys())
    min_sun = min_sunday(min_date)

    sunday = min_sun
    while sunday < max_date:
        print header(sunday, cell_width)
        for lineid in xrange(cell_height):
            print row(events_index, sunday, lineid, cell_width)
        sunday += datetime.timedelta(days=7)


def header(sunday, cell_width):
    hstr = ""
    for i in range(7):
        day = sunday + datetime.timedelta(days=i)
        datestr = MONTHS[day.month - 1] + " " + str(day.day)
        hstr += datestr.ljust(cell_width)
    return hstr


def row(events_index, sunday, lineid, cell_width):
    rowstr = ""
    for i in xrange(7):
        day = sunday + datetime.timedelta(days=i)
        rowstr += cell(events_index, day, lineid, cell_width).ljust(cell_width)
    return rowstr


def cell(events_index, date, lineid, cell_width):
    if date not in events_index or lineid > len(events_index[date]) - 1:
        return ""
    event_list = events_index[date]
    event = event_list[lineid]
    desc = event.desc[0:cell_width - 1]
    return desc