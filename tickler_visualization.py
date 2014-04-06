import argparse
import os

import print_calendar
import events


def main():
    parser = argparse.ArgumentParser("Visualize tickler file.")
    parser.add_argument("-x", help="cell width", type=int, default=11)
    parser.add_argument("-y", help="cell height", type=int, default=3)
    parser.add_argument("path", help="path to tickler file", type=str)
    args = parser.parse_args()

    if not os.path.isfile(args.path):
        print "Error: file \"{}\" does not exist.".format(args.path)
        return
    if args.x < 11:
        print "Error: cell width of {} is less than 11".format(args.x)
        return
    if args.y < 2:
        print "Error: cell height of {} is less than 2".format(args.y)
        return

    events_index = events.build_events_index(args.path)
    print_calendar.print_calendar(events_index, args.x, args.y)


if __name__ == "__main__":
    main()