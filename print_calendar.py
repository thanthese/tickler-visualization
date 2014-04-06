import datetime
import operator


_SUNDAY = 6
_MONTH = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
_WEEKDAY = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def _min_sunday(date):
    d = date
    while d.weekday() != _SUNDAY:
        d -= datetime.timedelta(days=1)
    return d


def _get_days(seed_day):
    return [seed_day + datetime.timedelta(days=i) for i in range(7)]


def _flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return []
    return reduce(operator.add, list_of_lists)


def print_calendar(events_index, w, h):
    """Takes an events index and the cell width and height."""

    min_date = min(events_index.keys() + [datetime.date.today()])
    max_date = max(events_index.keys())
    min_sun = _min_sunday(min_date)

    sunday = min_sun
    while sunday < max_date:
        days = _get_days(sunday)
        print ''.join([_day_header(d, w) for d in days])
        for lineid in xrange(h):
            print ''.join([_day_line(events_index, d, lineid, w, h) for d in days])
        _print_week_summary(events_index, sunday, w)
        sunday += datetime.timedelta(days=7)


def _day_header(day, w):
    if day == datetime.date.today():
        return "TODAY!".ljust(w)
    return "{} {}/{}".format(_WEEKDAY[day.weekday()], day.month, day.day).ljust(w)


def _day_line(index, date, lineid, w, h):
    if date not in index:
        return "".ljust(w)

    event_list = index[date]
    all_events_already_listed = lineid > len(index[date]) - 1
    if all_events_already_listed:
        return "".ljust(w)

    lastline = lineid + 1 == h
    overflow = len(event_list) > h
    if lastline and overflow:
        ids = [str(e.id) for e in event_list[lineid:]]
        return "[{}]".format(", ".join(ids)).ljust(w)

    event = event_list[lineid]
    format = lambda s: s.format(event.id, event.desc)[0:w - 1].ljust(w)
    if not event.is_through():
        return format("{}: {}")
    if event.is_through_beginning():
        return format("{}>: {}")
    if event.is_through_middle():
        return format("-{}-: {}")
    if event.is_through_end():
        return format("<{}: {}")
    return "ERROR".ljust(w)


def _print_week_summary(index, sunday, w):
    format = lambda e: "[{}]: #{} {}".format(e.id, e.type, e.desc.strip())
    events = _flatten([index[d] for d in _get_days(sunday) if d in index])
    keystrs = sorted(list(set(map(format, events))))
    if len(keystrs) > 0:
        width = w * 7
        print "----/ key /".ljust(width, '-')
        for k in keystrs:
            print k
        print "/ key /----".rjust(width, '-')
        print
