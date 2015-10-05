.. _site-configuration:

Site configuration
===================================

.. _temp-space:

Temporary space
----------------------------

.. warning:: Temporary space configuration will eventually be moved to
   configuration files, but currently these settings are in
   ``lib/spack/spack/__init__.py``

By default, Spack will try to do all of its building in temporary
space.  There are two main reasons for this.  First, Spack is designed
to run out of a user's home directory, and on may systems the home
directory is network mounted and potentially not a very fast
filesystem.  We create build stages in a temporary directory to avoid
this.  Second, many systems impose quotas on home directories, and
``/tmp`` or similar directories often have more available space.  This
helps conserve space for installations in users' home directories.

You can customize temporary directories by editing
``lib/spack/spack/__init__.py``.  Specifically, find this part of the file:

.. code-block:: python

   # Whether to build in tmp space or directly in the stage_path.
   # If this is true, then spack will make stage directories in
   # a tmp filesystem, and it will symlink them into stage_path.
   use_tmp_stage = True

   # Locations to use for staging and building, in order of preference
   # Use a %u to add a username to the stage paths here, in case this
   # is a shared filesystem.  Spack will use the first of these paths
   # that it can create.
   tmp_dirs = ['/nfs/tmp2/%u/spack-stage',
               '/var/tmp/%u/spack-stage',
               '/tmp/%u/spack-stage']

The ``use_tmp_stage`` variable controls whether Spack builds
**directly** inside the ``var/spack/`` directory.  Normally, Spack
will try to find a temporary directory for a build, then it *symlinks*
that temporary directory into ``var/spack/`` so that you can keep
track of what temporary directories Spack is using.

The ``tmp_dirs`` variable is a list of paths Spack should search when
trying to find a temporary directory.  They can optionally contain a
``%u``, which will substitute the current user's name into the path.
The list is searched in order, and Spack will create a temporary stage
in the first directory it finds to which it has write access.  Add
more elements to the list to indicate where your own site's temporary
directory is.


Profiling
~~~~~~~~~~~~~~~~~~~~~

Spack has some limited built-in support for profiling, and can report
statistics using standard Python timing tools.  To use this feature,
supply ``-p`` to Spack on the command line, before any subcommands.

.. _spack-p:

``spack -p``
^^^^^^^^^^^^^^^^^^

``spack -p`` output looks like this:

.. code-block:: sh

   $ spack -p graph dyninst
   o  dyninst
   |\
   | |\
   | o |  libdwarf
   |/ /
   o |  libelf
    /
   o  boost

         307670 function calls (305943 primitive calls) in 0.127 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      853    0.021    0.000    0.066    0.000 inspect.py:472(getmodule)
    51197    0.011    0.000    0.018    0.000 inspect.py:51(ismodule)
    73961    0.010    0.000    0.010    0.000 {isinstance}
     1762    0.006    0.000    0.053    0.000 inspect.py:440(getsourcefile)
    32075    0.006    0.000    0.006    0.000 {hasattr}
     1760    0.004    0.000    0.004    0.000 {posix.stat}
     2240    0.004    0.000    0.004    0.000 {posix.lstat}
     2602    0.004    0.000    0.011    0.000 inspect.py:398(getfile)
      771    0.004    0.000    0.077    0.000 inspect.py:518(findsource)
     2656    0.004    0.000    0.004    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
    30772    0.003    0.000    0.003    0.000 {method 'get' of 'dict' objects}
    ...

The bottom of the output shows the top most time consuming functions,
slowest on top.  The profiling support is from Python's built-in tool,
`cProfile
<https://docs.python.org/2/library/profile.html#module-cProfile>`_.
