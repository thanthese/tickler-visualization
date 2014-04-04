import print_calendar
import events


tickler_path = "/Users/thanthese/vimwiki/tickler.wiki"
cell_width = 11
cell_height = 3

events_index = events.build_events_index(tickler_path)
print_calendar.print_calendar(events_index, cell_width, cell_height)