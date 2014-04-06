import datetime
import re
import copy

_THROUGH_PATTERN = "\((through |-)(\d+)\w*\)"


def _load_events(path):
    with open(path) as f:
        lines = filter(lambda l: "#" in l, f.readlines())
    return [_Event(i, l) for i, l in enumerate(lines)]


def _build_date(datestr):
    year = int(datestr[0:2])
    month = int(datestr[3:5])
    day = int(datestr[6:8])
    return datetime.date(2000 + year, month, day)


def _build_through(desc):
    through = re.match(_THROUGH_PATTERN, desc)
    if through is None:
        return None
    return int(through.group(2))


class _Event():
    def __init__(self, id, line):
        datestr, type, desc = line.split(' ', 2)
        self.date = _build_date(datestr)
        self.type = type[1:]
        self.desc = re.sub(_THROUGH_PATTERN, "", desc)
        self.id = id
        self.through = _build_through(desc)
        self._original_date = self.date

    def set_date(self, date):
        self.date = date

    def is_through(self):
        return self.through is not None

    def is_through_beginning(self):
        return self.is_through() and self.date == self._original_date

    def is_through_middle(self):
        return (self.is_through()
                and not self.is_through_beginning()
                and not self.is_through_end())

    def is_through_end(self):
        return self.is_through() and self.date.day == self.through


def _build_index(events):
    index = {}
    for e in events:
        if e.date in index:
            index[e.date].append(e)
        else:
            index[e.date] = [e]
    return index


def _add_through_events(events):
    one_day = datetime.timedelta(days=1)
    through_events = []
    for e in events:
        if e.is_through():
            date = e.date
            while date.day != e.through:
                new_e = copy.copy(e)
                new_e.date = date + one_day
                through_events.append(new_e)
                date += one_day
    return through_events + events


def build_events_index(path):
    events = _load_events(path)
    events = _add_through_events(events)
    return _build_index(events)