import datetime
import re

tickler_path = "/Users/thanthese/vimwiki/tickler.wiki"
cell_width = 11
cell_height = 3
SUNDAY = 6


def get_events(path):
    with open(path) as f:
        return [Event(l) for l in (f.readlines()) if "#" in l]


def build_date(datestr):
    year = int(datestr[0:2])
    month = int(datestr[3:5])
    day = int(datestr[6:8])
    return datetime.date(2000 + year, month, day)


def build_through(desc):
    through = re.match(r"\(through (\d+)\w*\)", desc)
    if through is None:
        return None
    else:
        return int(through.group(1))


class Event():
    id = 0

    def __init__(self, line):
        datestr, type, desc = line.split(' ', 2)
        self.date = build_date(datestr)
        self.type = type[1:]
        self.desc = desc.rstrip()
        self.through = build_through(desc)
        self.id = Event.id
        Event.id += 1

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.date, self.type, self.desc, self.through)


def min_sunday(date):
    d = date
    while d.weekday() != SUNDAY:
        d -= datetime.timedelta(days=1)
    return d


def build_cal(events):
    cal = {}
    for e in events:
        if e.date in cal:
            cal[e.date].append(e)
        else:
            cal[e.date] = [e]
    return cal


def print_calendar(events):
    min_date = min(datetime.date.today(), events[0].date)
    max_date = events[-1].date
    min_sun = min_sunday(min_date)
    cal = build_cal(events)

    d = min_sun
    while d < max_date:
        print header(d)
        for r in xrange(cell_height):
            rowstr = ""
            for i in xrange(7):
                rowstr += row(cal, d + datetime.timedelta(days=i), r)
            print rowstr
        d += datetime.timedelta(days=7)


def header(date):
    s = ""
    for i in range(7):
        d = date + datetime.timedelta(days=i)
        p = "{}/{}".format(d.month, d.day)
        s += p.ljust(cell_width)
    return s


def row(cal, date, row_id):
    if date not in cal or row_id > len(cal[date]) - 1:
        return "".ljust(cell_width)
    event_list = cal[date]
    row = event_list[row_id]
    desc = row.desc[0:cell_width - 1].ljust(cell_width)
    return desc


events = get_events(tickler_path)
print_calendar(events)