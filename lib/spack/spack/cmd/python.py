import code
import os
import platform
from contextlib import closing

import spack

description = "Launch an interpreter as spack would launch a command"

def python(parser, args):
    console = code.InteractiveConsole()

    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with closing(open(startup_file)) as startup:
                console.runsource(startup.read(), startup_file, 'exec')

    console.interact("Spack version %s\nPython %s, %s %s"""
                     % (spack.spack_version, platform.python_version(),
                        platform.system(), platform.machine()))
