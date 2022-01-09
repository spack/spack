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
