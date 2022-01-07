# Installing Software from Source

## General Installation from a Local Source Tree

The following demonstrates installing a package from a local checkout into
the Spack installation tree:

    $ git clone git@github.com:BlueBrain/MVDTool.git
    $ cd MVDTool
    $ nvim CMakeLists.txt  # or other modifications of your choice
    $ spack dev-build -y --test=root mvdtool@123
    …
    [+] …/linux-rhel7-x86_64/gcc-9.3.0/mvdtool-123-imbxlf6…

Note the hash at the end of the last line, this can be used to refer to the
installation that was just performed.
This version of MVDTool can now be re-used by Spack to build other
software, when `^/imbxlf6` is appended to the appropriate
spec.

Similarly, Python based software can be installed the same way:

    $ git clone --recursive git@github.com:BlueBrain/MVDTool.git
    $ cd MVDTool
    $ nvim setup.py  # or other modifications of your choice
    $ spack dev-build -y --test=root py-mvdtool@123
    …
    [+] …/spack/linux-rhel7-x86_64/gcc-9.3.0/py-mvdtool-123-xilqkul…

Again, note the hash at the end of the line, this can be used to refer to
the installed package.
This Python module can now be used:

    $ module load python
    $ python -c 'import mvdtool; print(mvdtool.__file__)'
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ModuleNotFoundError: No module named 'mvdtool'
    $ spack load /xilq
    $ python -c 'import mvdtool; print(mvdtool.__file__)'
    …/linux-rhel7-x86_64/gcc-9.3.0/py-mvdtool-123-xilqkul…

## Interactively Building CMake-based Software

To interactively develop the CMake based packages, `spack setup` can be
used to emulate the traditional Cmake workflow.
**Please note that this seems to have been deprecated upstream and may not
always work**.

    $ git clone git@github.com:BlueBrain/MVDTool.git
    $ cd MVDTool
    $ spack setup mvdtool@develop
    [+] …/linux-rhel7-x86_64/gcc-9.3.0/mvdtool-develop-2qofleiy…


The last command will create an empty installation directory filled with
some bogus files (this is needed for eventual dependencies, but can also
interfere with builds).
As before, the hash contained in this line can be used to refer to the
package to be installed.
Also note that this created a file called `spconfig.py` in the current
directory, which will replace the `cmake` executable in the following:

    $ mkdir build && cd build
    $ spack build-env /2qof ../spconfig.py ..
    $ spack build-env /2qof make
    $ spack build-env /2qof make test
    $ spack build-env /2qof make install

Using `spack build-env /hash` is recommended to ensure that all of the
build-environment is available to the installation process, but may be
omitted, depending on the software installed.

The latter steps may be repeated while editing the source to provide an
interactive test environment similar to a purely CMake based workflow.
