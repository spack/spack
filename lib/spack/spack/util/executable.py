import os
import re
import subprocess
import spack.tty as tty


class Executable(object):
    """Class representing a program that can be run on the command line."""
    def __init__(self, name):
        self.exe = name.split(' ')


    def add_default_arg(self, arg):
        self.exe.append(arg)


    @property
    def command(self):
        return self.exe[0]


    def __call__(self, *args, **kwargs):
        """Run the executable with subprocess.check_output, return output."""
        return_output = kwargs.get("return_output", False)
        fail_on_error = kwargs.get("fail_on_error", True)

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn("Quotes in package command arguments can confuse shell scripts like configure.",
                     "The following arguments may cause problems when executed:",
                     str("\n".join(["    "+arg for arg in quoted_args])),
                     "Quotes aren't needed because spack doesn't use a shell.  Consider removing them")

        cmd = self.exe + list(args)
        tty.verbose(" ".join(cmd))

        if return_output:
            return subprocess.check_output(cmd)
        elif fail_on_error:
            return subprocess.check_call(cmd)
        else:
            return subprocess.call(cmd)

    def __repr__(self):
        return "<exe: %s>" % self.exe


def which(name, **kwargs):
    """Finds an executable in the path like command-line which."""
    path     = kwargs.get('path', os.environ.get('PATH', '').split(os.pathsep))
    required = kwargs.get('required', False)

    if not path:
        path = []

    for dir in path:
        exe = os.path.join(dir, name)
        if os.access(exe, os.X_OK):
            return Executable(exe)

    if required:
        tty.die("spack requires %s.  Make sure it is in your path." % name)
    return None
