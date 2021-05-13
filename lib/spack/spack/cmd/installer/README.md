This README is a guide for creating a Spack installer for Windows.  This is an .msi executable file
that users can run to install Spack like any other Windows binary.

Before proceeding, follow the setup instructions in
https://spack.readthedocs.io/en/latest/getting_started.html for getting
Spack operational without the installer.

# Step 1: Install prerequisites

The only additional prerequisite for making the installer is Wix.  Wix is a utility used for .msi creation and
can be downloaded and installed at https://wixtoolset.org/releases/.  The Visual Studio
extensions are not necessary. 

# Step 2: Make the installer

To actually make the installer, start by running ``spack_cmd.bat`` from
Windows Explorer as if you were using Spack through it (see the documentation above).
You will aneed to add the CMake executable provided by Visual Studio
to your path, which will look something like:

``C:\Program Files (x86)\Microsoft Visual Studio\<year>\<distribution>\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake``

**IMPORTANT**: If you use Tab to complete any part of this path, the console will automatically
add quotation marks to the start and the end since it will see the spaces and want to parse the
whole of it as a string. This is incorrect for our purposes so before submitting the command,
ensure that the quotes are removed. You will encounter configuration errors if you fail to do this. 

``spack_cmd.bat`` will produce a DOS console window. Navigate to your
``spack_install`` directory (i.e. where you placed ``spack_cmd.bat``), and
create a new directory to store the installation (say, ``tmp``). This ``tmp``
directory must exist for the following commands to not fail.

There are two ways to create the installer. If you would like to create it
from a release version of Spack, say, 0.16.0, and store it in ``tmp``, you
can use the following command:

``spack make-installer -v 0.16.0 tmp``

The path to ``tmp`` can be either relative or absolute, but again, the
directory itself must already exist.

Alternatively, if you would like to build the installer using a local
checkout of Spack source (release or development), you can use the
-s flag to specify the directory where that checkout is. For example,
if you are doing development in a directory called ``spack-develop``
and want to generate an installer with the source there, you can use:

``spack make-installer -s spack-develop tmp``

Similar to the -v build, the ``spack-develop`` directory may be an absolute
path or relative to the current working directory. The entire contents of the 
specified directory will be included in the installed (e.g. .git files or 
local changes).

# Step 3: Run the installer

Regardless of your method, a file called ``Spack.msi`` will be created
inside the ``tmp`` directory, which can then be run from Windows Explorer
like any other installer. After accepting the terms of service, select
where on your computer you would like Spack installed, and after a few minutes
Spack will be installed and ready for use.

If your Spack installation needs to be modified, repaired, or uninstalled, 
you can do any of these things by rerunning Spack.msi.

Running the installer also creates a shortcut on your desktop that, when launched,
will load a console identical to ``spack_cmd``, but with its initial directory
being wherever Spack was installed on your computer. You may then proceed using Spack
through this console as you would through ``spack_cmd``.
