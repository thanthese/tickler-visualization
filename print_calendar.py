import datetime
import operator


SUNDAY = 6
MONTH = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
WEEKDAY = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


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
            print row(events_index, sunday, lineid, cell_width, cell_height)
        print_week_summary(events_index, sunday, cell_width)
        sunday += datetime.timedelta(days=7)


def header(sunday, cell_width):
    hstr = ""
    for i in range(7):
        day = sunday + datetime.timedelta(days=i)
        if day == datetime.date.today():
            datestr = "TODAY!"
        else:
            datestr = "{} {}/{}".format(WEEKDAY[day.weekday()], day.month, day.day)
        hstr += datestr.ljust(cell_width)
    return hstr


def row(events_index, sunday, lineid, cell_width, cell_height):
    rowstr = ""
    for i in xrange(7):
        day = sunday + datetime.timedelta(days=i)
        rowstr += cell(events_index, day, lineid, cell_width, cell_height).ljust(cell_width)
    return rowstr


def cell(events_index, date, lineid, cell_width, cell_height):
    if date not in events_index:
        return ""

    event_list = events_index[date]
    out_of_events = lineid > len(events_index[date]) - 1
    if out_of_events:
        return ""

    lastline = lineid + 1 == cell_height
    overflow = len(event_list) > cell_height
    if lastline and overflow:
        return '[' + ", ".join([str(e.id) for e in event_list[lineid:]]) + ']'

    event = event_list[lineid]
    return "{}: {}".format(event.id, event.desc)[0:cell_width - 1]

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return []
    return reduce(operator.add, list_of_lists)

def print_week_summary(events_index, sunday, cell_width):
    format = lambda e: "[{}]: #{} {}".format(e.id, e.type, e.desc.strip())
    days = [sunday + datetime.timedelta(days=i) for i in range(7)]
    events = flatten([events_index[d] for d in days if d in events_index])
    keys = sorted(list(set(map(format, events))))
    if len(keys) > 0:
        width = cell_width * 7
        print "----/ key /".ljust(width, '-')
        for k in keys:
            print k
        print "".ljust(width, '-')
