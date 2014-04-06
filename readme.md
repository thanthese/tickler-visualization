This project converts a [tickler file][tf] that looks roughly like this:

[tf]: http://en.wikipedia.org/wiki/Tickler_file

    14.04.06u nothing special
    14.04.07m not an appointment
    14.04.08t #appt something special to do
    14.04.10r #bday john smith
    14.04.12s not an appointment
    14.04.14m #appt (through 16) long running event

into something that looks more like this:

    sun 3/30   mon 3/31   tue 4/1    wed 4/2    thu 4/3    fri 4/4    TODAY!



    sun 4/6    mon 4/7    tue 4/8    wed 4/9    thu 4/10   fri 4/11   sat 4/12
                          0: somethi            1: john sm


    ----/ key /------------------------------------------------------------------
    [0]: #appt something special to do
    [1]: #bday john smith
    -----------------------------------------------------------------------------

    sun 4/13   mon 4/14   tue 4/15   wed 4/16   thu 4/17   fri 4/18   sat 4/19
               2>:  long  <2>:  long <2:  long


    ----/ key /------------------------------------------------------------------
    [2]: #appt long running event
    -----------------------------------------------------------------------------

### Tickler file syntax

The general form is `date type through time description`, where

- **date**: takes the form `YY.MM.DD` (plus anything else with no whitespace)

- *type*: takes the form `#what` where `what` is the type of event (`bday`, `anniversary`,
`holiday`, etc...). This will be from the short description.

- *through*: a special string of the form `(through N..)` or `(-N..)`, where `N` is the day
of the month and `..` can be anything. Defines how events repeat (from this day *through until* this day).
Note that `N` cannot be a full month or more away.

- *time*: by convention, something like `5:30pm` goes here

- *description*: description of event.

By convention the whole line is less than 80 characters.

### Usage

Run something like this in the terminal:

    $ python tickler_visualization sample_tickler.txt

or for usage

    $ python tickler_visualization -h

### Limitations

This is pretty specific to the way I work and the way I structure my calendar and files.
I don't expect anyone else would find it terribly useful.

### License

MIT

