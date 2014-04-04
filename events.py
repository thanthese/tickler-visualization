import datetime
import re

through_pattern = "\(through (\d+)\w*\) "


def load_events(path):
    with open(path) as f:
        lines = filter(lambda l: "#" in l, f.readlines())
    return [Event(i, l) for i, l in enumerate(lines)]


def build_date(datestr):
    year = int(datestr[0:2])
    month = int(datestr[3:5])
    day = int(datestr[6:8])
    return datetime.date(2000 + year, month, day)


def build_through(desc):
    through = re.match(through_pattern, desc)
    if through is None:
        return None
    else:
        return int(through.group(1))


class Event():
    def __init__(self, id, line):
        datestr, type, desc = line.split(' ', 2)
        self.date = build_date(datestr)
        self.type = type[1:]
        self.through = build_through(desc)
        self.desc = re.sub(through_pattern, "", desc)
        self.id = id

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.date, self.type, self.desc, self.through)


def _build_events_index(events):
    index = {}
    for e in events:
        if e.date in index:
            index[e.date].append(e)
        else:
            index[e.date] = [e]
    return index


def build_events_index(path):
    events = load_events(path)[0:5]  # remove range
    return _build_events_index(events)