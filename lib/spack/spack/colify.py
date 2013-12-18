# colify
# By Todd Gamblin, tgamblin@llnl.gov
#
# Takes a list of items as input and finds a good columnization of them,
# similar to how gnu ls does.  You can pipe output to this script and
# get a tight display for it.  This supports both uniform-width and
# variable-width (tighter) columns.
#
# Run colify -h for more information.
#
import os
import sys
import fcntl
import termios
import struct

def get_terminal_size():
    """Get the dimensions of the console."""
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])


class ColumnConfig:
    def __init__(self, cols):
        self.cols = cols
        self.line_length = 0
        self.valid = True
        self.widths = [0] * cols

    def __repr__(self):
        attrs = [(a,getattr(self, a)) for a in dir(self) if not a.startswith("__")]
        return "<Config: %s>" % ", ".join("%s: %r" % a for a in attrs)


def config_variable_cols(elts, console_cols, padding):
    # Get a bound on the most columns we could possibly have.
    lengths = [len(elt) for elt in elts]
    max_cols = max(1, console_cols / (min(lengths) + padding))
    max_cols = min(len(elts), max_cols)

    configs = [ColumnConfig(c) for c in xrange(1, max_cols+1)]
    for elt, length in enumerate(lengths):
        for i, conf in enumerate(configs):
            if conf.valid:
                col = elt / ((len(elts) + i) / (i + 1))
                padded = length
                if col < i:
                    padded += padding

                if conf.widths[col] < padded:
                    conf.line_length += padded - conf.widths[col]
                    conf.widths[col] = padded
                    conf.valid = (conf.line_length < console_cols)

    try:
        config = next(conf for conf in reversed(configs) if conf.valid)
    except StopIteration:
        # If nothing was valid the screen was too narrow -- just use 1 col.
        config = configs[0]

    config.widths = [w for w in config.widths if w != 0]
    config.cols = len(config.widths)
    return config


def config_uniform_cols(elts, console_cols, padding):
    max_len = max(len(elt) for elt in elts) + padding
    cols = max(1, console_cols / max_len)
    cols = min(len(elts), cols)
    config = ColumnConfig(cols)
    config.widths = [max_len] * cols
    return config


def isatty(ostream):
    force = os.environ.get('COLIFY_TTY', 'false').lower() != 'false'
    return force or ostream.isatty()


def colify(elts, **options):
    # Get keyword arguments or set defaults
    output       = options.get("output", sys.stdout)
    indent       = options.get("indent", 0)
    padding      = options.get("padding", 2)

    # elts needs to be an array of strings so we can count the elements
    elts = [str(elt) for elt in elts]
    if not elts:
        return

    if not isatty(output):
        for elt in elts:
            output.write("%s\n" % elt)
        return

    console_cols = options.get("cols", None)
    if not console_cols:
        console_cols, console_rows = get_terminal_size()
    elif type(console_cols) != int:
        raise ValueError("Number of columns must be an int")
    console_cols = max(1, console_cols - indent)

    method = options.get("method", "variable")
    if method == "variable":
        config = config_variable_cols(elts, console_cols, padding)
    elif method == "uniform":
        config = config_uniform_cols(elts, console_cols, padding)
    else:
        raise ValueError("method must be one of: " + allowed_methods)

    cols = config.cols
    formats = ["%%-%ds" % width for width in config.widths[:-1]]
    formats.append("%s")  # last column has no trailing space

    rows = (len(elts) + cols - 1) / cols
    rows_last_col = len(elts) % rows

    for row in xrange(rows):
        output.write(" " * indent)
        for col in xrange(cols):
            elt = col * rows + row
            output.write(formats[col] % elts[elt])

        output.write("\n")
        row += 1
        if row == rows_last_col:
            cols -= 1


if __name__ == "__main__":
    import optparse

    cols, rows = get_terminal_size()
    parser = optparse.OptionParser()
    parser.add_option("-u", "--uniform", action="store_true", default=False,
                      help="Use uniformly sized columns instead of variable-size.")
    parser.add_option("-p", "--padding", metavar="PADDING", action="store",
                      type=int, default=2, help="Spaces to add between columns.  Default is 2.")
    parser.add_option("-i", "--indent", metavar="SPACES", action="store",
                      type=int, default=0, help="Indent the output by SPACES.  Default is 0.")
    parser.add_option("-w", "--width", metavar="COLS", action="store",
                      type=int, default=cols, help="Indent the output by SPACES.  Default is 0.")
    options, args = parser.parse_args()

    method = "variable"
    if options.uniform:
        method = "uniform"

    if sys.stdin.isatty():
        parser.print_help()
        sys.exit(1)
    else:
        colify([line.strip() for line in sys.stdin], method=method, **options.__dict__)
