import spack.tty as tty

def required(obj, attr_name):
    """Ensure that a class has a required attribute."""
    if not hasattr(obj, attr_name):
        tty.die("No required attribute '%s' in class '%s'"
                % (attr_name, obj.__class__.__name__))


def setdefault(obj, name, value):
    """Like dict.setdefault, but for objects."""
    if not hasattr(obj, name):
        setattr(obj, name, value)
    return getattr(obj, name)
