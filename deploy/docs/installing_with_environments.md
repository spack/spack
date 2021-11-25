# Installing Software in Environments

Spack environments are conceptually somewhat similar to Python's
`virtualenv`, in that they allow the user to specify which packages should
be present in the current shell environment after activation.
But they normally share the installation directory of the software with
regular Spack installations, and also provide a UNIX-like tree hidden in
the environment directory.

We can start by creating an environment:

    $ spack env create -d spamhameggs

and then activating it, and fixing the configuration to consider all
software together:

    $ spack env activate -d spamhameggs
    $ spack config add config:spack:concretization=together

This will make sure that every package is only built once, in the specified
version.

All subsequent actions now act on this environment. To leave the
environment, use the command `despacktivate` or `spack env deactivate`.

First, we add TouchDetector to it:

    $ spack add touchdetector

Now we can tell see which software needs to be installed:

    $ spack concretize
    ==> Concretized touchdetector
     -   lhp5vxl  touchdetector@5.5.0%gcc@9.3.0~ipo~openmp
    …
     -   72bpagc      ^mvdtool@2.3.5%gcc@9.3.0~ipo+mpi
     -   axln3ax          ^libsonata@0.1.6%gcc@9.3.0~ipo+mpi
    …

Now we can add an already existing source directory for the dependency of
`mvdtool`:

    $ git clone git@github.com:BlueBrain/MVDTool.git
    $ spack develop -p ${PWD}/MVDTool --no-clone mvdtool@develop

And after another round of concretization:

    $ spack concretize -f
    ==> Concretized touchdetector
     -   nwzcdxp  touchdetector@5.5.0%gcc@9.3.0~ipo~openmp
    …
     -   vs2omx5      ^mvdtool@develop%gcc@9.3.0~ipo+mpi dev_path=…/MVDTool
     -   axln3ax          ^libsonata@0.1.6%gcc@9.3.0~ipo+mpi
    …

We can now install everything together:

    $ spack install

Modifying the source of MVDTool and retriggering a build:

    $ spack install

Should now rebuild both `mvdtool` and `touchdetector`.

## Python Packages

You should also be able to install and use Python packages like the above.
Re-using the **active** environment from above, first cleaning it:

    $ spack rm touchdetector

Then adding `py-mvdtool` and telling Spack to use the local sources:

    $ spack add py-mvdtool@develop
    $ spack develop -p ${PWD}/MVDTool --no-clone py-mvdtool@develop

And install everything:

    $ spack install

You may need to "refresh" the environment by deactivating and
re-activating (to ensure that any new Python paths are included in the
environment):

    $ spack env deactivate
    $ spack env activate -d spamhameggs

And finally, you should be able to use the Python module without any proper
modules loaded:

    $ python -c 'import mvdtool; print(mvdtool.__file__)'

Modifying the packages marked as to "develop" will cause `spack install` to
re-install them and their dependencies as well.
This should lend itself to a good interactive Python development
environment.
