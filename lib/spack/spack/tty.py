import sys
import spack

indent = "  "

def escape(s):
    """Returns a TTY escape code if stdout is a tty, otherwise empty string"""
    if sys.stdout.isatty():
        return "\033[{}m".format(s)
    return ''

def color(n):
    return escape("0;{}".format(n))

def bold(n):
    return escape("1;{}".format(n))

def underline(n):
    return escape("4;{}".format(n))

blue   = bold(34)
white  = bold(39)
red    = bold(31)
yellow = underline(33)
green  = bold(92)
gray   = bold(30)
em     = underline(39)
reset  = escape(0)

def msg(msg, *args, **kwargs):
    color = kwargs.get("color", blue)
    print "{}==>{} {}{}".format(color, white, str(msg), reset)
    for arg in args: print indent + str(arg)

def info(msg, *args, **kwargs):
    color = kwargs.get("color", blue)
    print "{}==>{} {}".format(color, reset, str(msg))
    for arg in args: print indent + str(arg)

def verbose(*args):
    if spack.verbose: msg(*args, color=green)

def debug(*args):
    if spack.debug: msg(*args, color=red)

def error(msg, *args):
    print "{}Error{}: {}".format(red, reset, str(msg))
    for arg in args: print indent + str(arg)

def warn(msg, *args):
    print "{}Warning{}: {}".format(yellow, reset, str(msg))
    for arg in args: print indent + str(arg)

def die(msg, *args):
    error(msg, *args)
    sys.exit(1)

def pkg(msg):
    """Outputs a message with a package icon."""
    import platform
    from version import Version

    mac_ver = platform.mac_ver()[0]
    if mac_ver and Version(mac_ver) >= Version('10.7'):
        print u"\U0001F4E6" + indent,
    else:
        print '{}[+]{} '.format(green, reset),
    print msg
