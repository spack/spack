This README is a guide for creating a Spack installer for Windows using the
``make-installer`` command. The installer is an executable file that users
can run to install Spack like any other Windows binary.

Before proceeding, follow the setup instructions in Steps 1 and 2 of
[Getting Started on Windows](https://spack.readthedocs.io/en/latest/getting_started.html#windows_support).

# Step 1: Install prerequisites

The only additional prerequisite for making the installer is Wix. Wix is a
utility used for .msi creation and can be downloaded and installed at
https://wixtoolset.org/releases/. The Visual Studio extensions are not
necessary.

# Step 2: Make the installer

To use Spack, run ``spack_cmd.bat``. This will provide a Windows command
prompt with an environment properly set up with Spack and its prerequisites.

Ensure that Python and CMake are on your PATH. If needed, you may add the
CMake executable provided by Visual Studio to your path, which will look
something like:

``C:\Program Files (x86)\Microsoft Visual Studio\<year>\<distribution>\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake``

**IMPORTANT**: If you use Tab to complete any part of this path, the console
will automatically add quotation marks to the start and the end since it will
see the spaces and want to parse the whole of it as a string. This is
incorrect for our purposes so before submitting the command, ensure that the
quotes are removed. You will encounter configuration errors if you fail to do
this.

There are two ways to create the installer using Spack's ``make-installer``
command. The recommended method is to build the installer using a local
checkout of Spack source (release or development), using the
`-s` flag to specify the directory where the local checkout is. For
example, if the local checkout is in a directory called ``spack-develop``
and want to generate an installer with the source there, you can use:

``spack make-installer -s spack-develop tmp``

Both the Spack source directory (e.g. ``spack-develop``) and installer
destination directory (e.g. ``tmp``) may be an absolute path or relative to
the current working directory. The entire contents of the specified
directory will be included in the installer (e.g. .git files or local
changes).

Alternatively, if you would like to create an installer from a release version
of Spack, say, 0.16.0, and store it in ``tmp``, you can use the following
command:

``spack make-installer -v 0.16.0 tmp``

**IMPORTANT**: Windows features are not currently supported in Spack's
official release branches, so an installer created using this method will
*not* run on Windows.

Regardless of your method, a file called ``Spack.exe`` will be created
inside the destination directory. This executable bundles the Spack installer
(``Spack.msi`` also located in destination directory) and the git installer.

# Step 3: Run the installer

After accepting the terms of service, select where on your computer you would
like Spack installed, and after a few minutes Spack, Python and git will be
installed and ready for use.

**IMPORTANT**: To avoid permissions issues, it is recommended to select an
install location other than ``C:\Program Files``.

**IMPORTANT**: There is a specific option that must be chosen when letting Git
install. When given the option of adjusting your ``PATH``, choose the
``Git from the command line and also from 3rd-party software`` option. This will
automatically update your ``PATH`` variable to include the ``git`` command.
Certain Spack commands expect ``git`` to be part of the ``PATH``. If this step
is not performed properly, certain Spack comands will not work.

If your Spack installation needs to be modified, repaired, or uninstalled,
you can do any of these things by rerunning ``Spack.exe``.

Running the installer creates a shortcut on your desktop that, when
launched, will run ``spack_cmd.bat`` and launch a console with its initial
directory being wherever Spack was installed on your computer. If Python is
found on your PATH, that will be used. If not, the Python included with the
installer will be used when running Spack.
