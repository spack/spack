import sys
import spack
from spack.color import *

indent = "  "

def msg(message, *args):
    cprint("@*b{==>} @*w{%s}" % cescape(message))
    for arg in args:
        print indent + str(arg)


def info(message, *args, **kwargs):
    format = kwargs.get('format', '*b')
    cprint("@%s{==>} %s" % (format, cescape(message)))
    for arg in args:
        print indent + str(arg)


def verbose(message, *args):
    if spack.verbose:
        info(message, *args, format='*g')


def debug(*args):
    if spack.debug:
        info("Debug: " + message, *args, format='*c')


def error(message, *args):
    info("Error: " + message, *args, format='*r')


def warn(message, *args):
    info("Warning: " + message, *args, format='*Y')


def die(message, *args):
    error(message, *args)
    sys.exit(1)


def pkg(message):
    """Outputs a message with a package icon."""
    import platform
    from version import Version

    mac_ver = platform.mac_ver()[0]
    if mac_ver and Version(mac_ver) >= Version('10.7'):
        print u"\U0001F4E6" + indent
    else:
        cwrite('@*g{[+]} ')
    print message


def get_number(prompt, **kwargs):
    default = kwargs.get('default', None)
    abort = kwargs.get('abort', None)

    if default is not None and abort is not None:
        prompt += ' (default is %s, %s to abort) ' % (default, abort)
    elif default is not None:
        prompt += ' (default is %s) ' % default
    elif abort is not None:
        prompt += ' (%s to abort) ' % abort

    number = None
    while number is None:
        ans = raw_input(prompt)
        if ans == str(abort):
            return None

        if ans:
            try:
                number = int(ans)
                if number < 1:
                    msg("Please enter a valid number.")
                    number = None
            except ValueError:
                msg("Please enter a valid number.")
        elif default is not None:
            number = default
    return number
