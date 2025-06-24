.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _getting_started:

===============
Getting Started
===============

Getting Spack is easy.  You can clone it from the `GitHub repository
<https://github.com/spack/spack>`_ using this command:

.. code-block:: console

   $ git clone --depth=2 https://github.com/spack/spack.git

This will create a directory called ``spack``. Once you have cloned Spack, we recommend sourcing the appropriate script for your shell:

.. tab-set::

   .. tab-item:: bash/zsh/sh

      .. code-block:: console

         $ . spack/share/spack/setup-env.sh

   .. tab-item:: tcsh/csh

      .. code-block:: console

         $ source spack/share/spack/setup-env.csh

   .. tab-item:: fish

      .. code-block:: console

         $ . spack/share/spack/setup-env.fish

Now you're ready to use Spack!

-----------------------------
List packages you can install
-----------------------------

Once Spack is ready you can list all the packages it knows about with the following command:

.. code-block:: console

   $ spack list

If you want to get more information on a specific package, for instance ``hdf5``, you can use:

.. code-block:: console

   $ spack info hdf5

This command shows information about ``hdf5``, including a brief description, the versions of the package Spack knows about, and all the options you can activate when installing.

As you can see it's quite simple to gather basic information on packages, before you install them!

.. admonition:: Slowdown on the very first command
   :class: warning
   :collapsible:

   The very first command run with Spack will take a while to finish, as Spack has to build a few caches to speed-up further command execution.
   This will be just a one-off slowdown though, and subsequent command execution is much faster.

-----------------------------
Installing your first package
-----------------------------

To install most packages, Spack needs a compiler suite to be available.
To search your machine for available compilers, you can run:

.. code-block:: console

   $ spack compiler find

The command shows users if any compiler was found, and where its configuration is stored.
If the search was successful, you can now list known compilers, and get an output similar to the following:

.. code-block:: console

   $ spack compiler list
   ==> Available compilers
   -- gcc ubuntu20.04-x86_64 ---------------------------------------
   [e]  gcc@9.4.0  [e]  gcc@8.4.0  [e]  gcc@10.5.0

If no compiler was found, you need either:

* To install further prerequisites, for which we refer to :ref:`verify-spack-prerequisites`, and repeat the search above.
* To register a buildcache that provides a compiler already available as a binary

Once a compiler is available, by any of the above means, you can proceed installing your first package:

.. code-block:: console

   $ spack install tcl

The output of this command should look similar to the following:

.. code-block:: text

   [+] /usr (external gcc-10.5.0-zmjbkxxgltryn6hxwzan35qxxw4skbgl)
   ==> No binary for compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx found: installing from source
   ==> Installing compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx [2/7]
   [+] /usr (external glibc-2.31-rawvy4pmq4nwhk6ipqnesomvstwyopxq)
   ==> No binary for gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj found: installing from source
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/c6/c65a9d2b2d4eef67ab5cb0684d706bb9f005bb2be94f53d82683d7055bdb837c
   ==> No patches needed for compiler-wrapper
   ==> Installing gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj [4/7]
   ==> compiler-wrapper: Executing phase: 'install'
   ==> No patches needed for gcc-runtime
   ==> compiler-wrapper: Successfully installed compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx
     Stage: 0.00s.  Install: 0.00s.  Post-install: 0.01s.  Total: 0.07s
   [+] /home/spack/.local/spack/opt/linux-icelake/compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx
   ==> gcc-runtime: Executing phase: 'install'
   ==> gcc-runtime: Successfully installed gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj
     Stage: 0.00s.  Install: 0.04s.  Post-install: 0.05s.  Total: 0.14s
   [+] /home/spack/.local/spack/opt/linux-icelake/gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj
   ==> No binary for gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm found: installing from source
   ==> Installing gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm [5/7]
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/dd/dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3.tar.gz
   ==> No patches needed for gmake
   ==> gmake: Executing phase: 'install'
   ==> gmake: Successfully installed gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm
     Stage: 0.05s.  Install: 15.91s.  Post-install: 0.01s.  Total: 16.00s
   [+] /home/spack/.local/spack/opt/linux-icelake/gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm
   ==> No binary for zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz found: installing from source
   ==> Installing zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz [6/7]
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/a7/a73343c3093e5cdc50d9377997c3815b878fd110bf6511c2c7759f2afb90f5a3.tar.gz
   ==> No patches needed for zlib-ng
   ==> zlib-ng: Executing phase: 'autoreconf'
   ==> zlib-ng: Executing phase: 'configure'
   ==> zlib-ng: Executing phase: 'build'
   ==> zlib-ng: Executing phase: 'install'
   ==> zlib-ng: Successfully installed zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz
     Stage: 0.03s.  Autoreconf: 0.00s.  Configure: 3.63s.  Build: 2.52s.  Install: 0.09s.  Post-install: 0.02s.  Total: 6.49s
   [+] /home/spack/.local/spack/opt/linux-icelake/zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz
   ==> No binary for tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv found: installing from source
   ==> Installing tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv [7/7]
   ==> Fetching https://mirror.spack.io/_source-cache/archive/26/26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6.tar.gz
       [100%]   10.35 MB @   48.5 MB/s
   ==> No patches needed for tcl
   ==> tcl: Executing phase: 'autoreconf'
   ==> tcl: Executing phase: 'configure'
   ==> tcl: Executing phase: 'build'
   ==> tcl: Executing phase: 'install'
   ==> tcl: Successfully installed tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv
     Stage: 0.46s.  Autoreconf: 0.00s.  Configure: 9.25s.  Build: 1m 8.71s.  Install: 3.32s.  Post-install: 0.68s.  Total: 1m 22.61s
   [+] /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv

Congratulations! You just installed your first package with Spack!

-----------------------------------
Use the software you just installed
-----------------------------------

Once you installed ``tcl`` you can immediately use it starting the ``tcsh`` with its absolute path:

.. code-block:: console

   $ /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv/bin/tclsh
   >% echo "Hello world!"
   Hello world!

This works because of how Spack builds packages, setting the ``RPATH`` of their dependencies, but using such a long absolute path is not the most ergonomic way to refer to an executable.

The simplest way to have ``tcsh`` directory added to your ``PATH`` is to:

.. code-block:: console

   $ spack load tcl

Now the environment of the current shell has been modified, and you can use:

.. code-block:: console

   $ tcsh

directly. To undo these modifications, you can:

.. code-block:: console

   $ spack unload tcl

.. admonition:: Environments and views
   :class: tip

   A better way to install and load a set of packages that are frequently used are Spack Environments with views.
   The discussion of this topic is outside of the boundary of this "Getting Started" guide, and we refer to :ref:`environments` for more information.

----------
Next steps
----------

This section just helped you getting Spack installed, and running, quickly.
There are further resources in the documentation, for more advanced use cases:

1. **Getting information on packages**: see :ref:`basic-list-and-info-packages`
2. **Verify Spack prerequisites on a given system**: see :ref:`verify-spack-prerequisites`


-----------------------
Utilities Configuration
-----------------------

Although Spack does not need installation *per se*, it does rely on
other packages to be available on its host system.  If those packages
are out of date or missing, then Spack will not work.  Sometimes, an
appeal to the system's package manager can fix such problems.  If not,
the solution is to have Spack install the required packages, and then
have Spack use them.

For example, if ``curl`` doesn't work, one could use the following steps
to provide Spack a working ``curl``:

.. code-block:: console

    $ spack install curl
    $ spack load curl

or alternately:

.. code-block:: console

    $ spack module tcl loads curl >>~/.bashrc

or if environment modules don't work:

.. code-block:: console

    $ export PATH=`spack location --install-dir curl`/bin:$PATH


External commands are used by Spack in two places: within core Spack,
and in the package recipes. The bootstrapping procedure for these two
cases is somewhat different, and is treated separately below.

^^^^^^^^^^^^^^^^^^^^
Core Spack Utilities
^^^^^^^^^^^^^^^^^^^^

Core Spack uses the following packages, mainly to download and unpack
source code: ``curl``, ``env``, ``git``, ``go``, ``hg``, ``svn``,
``tar``, ``unzip``, ``patch``

As long as the user's environment is set up to successfully run these
programs from outside of Spack, they should work inside of Spack as
well.  They can generally be activated as in the ``curl`` example above;
or some systems might already have an appropriate hand-built
environment module that may be loaded.  Either way works.

A few notes on specific programs in this list:

""""""""""""""""""""""""""
curl, git, Mercurial, etc.
""""""""""""""""""""""""""

Spack depends on curl to download tarballs, the format that most
Spack-installed packages come in.  Your system's curl should always be
able to download unencrypted ``http://``.  However, the curl on some
systems has problems with SSL-enabled ``https://`` URLs, due to
outdated / insecure versions of OpenSSL on those systems.  This will
prevent Spack from installing any software requiring ``https://``
until a new curl has been installed, using the technique above.

.. warning::

   remember that if you install ``curl`` via Spack that it may rely on a
   user-space OpenSSL that is not upgraded regularly.  It may fall out of
   date faster than your system OpenSSL.

Some packages use source code control systems as their download method:
``git``, ``hg``, ``svn`` and occasionally ``go``.  If you had to install
a new ``curl``, then chances are the system-supplied version of these
other programs will also not work, because they also rely on OpenSSL.
Once ``curl`` has been installed, you can similarly install the others.


^^^^^^^^^^^^^^^^^
Package Utilities
^^^^^^^^^^^^^^^^^

Spack may also encounter bootstrapping problems inside a package's
``install()`` method.  In this case, Spack will normally be running
inside a *sanitized build environment*.  This includes all of the
package's dependencies, but none of the environment Spack inherited
from the user: if you load a module or modify ``$PATH`` before
launching Spack, it will have no effect.

In this case, you will likely need to use the ``--dirty`` flag when
running ``spack install``, causing Spack to **not** sanitize the build
environment.  You are now responsible for making sure that environment
does not do strange things to Spack or its installs.

Another way to get Spack to use its own version of something is to add
that something to a package that needs it.  For example:

.. code-block:: python

   depends_on('binutils', type='build')

This is considered best practice for some common build dependencies,
such as ``autotools`` (if the ``autoreconf`` command is needed) and
``cmake`` --- ``cmake`` especially, because different packages require
a different version of CMake.

""""""""
binutils
""""""""

.. https://groups.google.com/forum/#!topic/spack/i_7l_kEEveI

Sometimes, strange error messages can happen while building a package.
For example, ``ld`` might crash.  Or one receives a message like:

.. code-block:: console

   ld: final link failed: Nonrepresentable section on output


or:

.. code-block:: console

   ld: .../_fftpackmodule.o: unrecognized relocation (0x2a) in section `.text'

These problems are often caused by an outdated ``binutils`` on your
system.  Unlike CMake or Autotools, adding ``depends_on('binutils')`` to
every package is not considered a best practice because every package
written in C/C++/Fortran would need it.  A potential workaround is to
load a recent ``binutils`` into your environment and use the ``--dirty``
flag.

-----------
GPG Signing
-----------

.. _cmd-spack-gpg:

^^^^^^^^^^^^^
``spack gpg``
^^^^^^^^^^^^^

Spack has support for signing and verifying packages using GPG keys. A
separate keyring is used for Spack, so any keys available in the user's home
directory are not used.

^^^^^^^^^^^^^^^^^^
``spack gpg init``
^^^^^^^^^^^^^^^^^^

When Spack is first installed, its keyring is empty. Keys stored in
:file:`var/spack/gpg` are the default keys for a Spack installation. These
keys may be imported by running ``spack gpg init``. This will import the
default keys into the keyring as trusted keys.

^^^^^^^^^^^^^
Trusting keys
^^^^^^^^^^^^^

Additional keys may be added to the keyring using
``spack gpg trust <keyfile>``. Once a key is trusted, packages signed by the
owner of the key may be installed.

^^^^^^^^^^^^^
Creating keys
^^^^^^^^^^^^^

You may also create your own key so that you may sign your own packages using
``spack gpg create <name> <email>``. By default, the key has no expiration,
but it may be set with the ``--expires <date>`` flag (see the ``gnupg2``
documentation for accepted date formats). It is also recommended to add a
comment as to the use of the key using the ``--comment <comment>`` flag. The
public half of the key can also be exported for sharing with others so that
they may use packages you have signed using the ``--export <keyfile>`` flag.
Secret keys may also be later exported using the
``spack gpg export <location> [<key>...]`` command.

.. note::

   Key creation speed
      The creation of a new GPG key requires generating a lot of random numbers.
      Depending on the entropy produced on your system, the entire process may
      take a long time (*even appearing to hang*). Virtual machines and cloud
      instances are particularly likely to display this behavior.

      To speed it up, you may install tools like ``rngd``, which is
      usually available as a package in the host OS.  For example, on an
      Ubuntu machine you need to give the following commands:

      .. code-block:: console

         $ sudo apt-get install rng-tools
         $ sudo rngd -r /dev/urandom

      before generating the keys.

      Another alternative is ``haveged``, which can be installed on
      RHEL/CentOS machines as follows:

      .. code-block:: console

         $ sudo yum install haveged
         $ sudo chkconfig haveged on

      `This Digital Ocean tutorial
      <https://www.digitalocean.com/community/tutorials/how-to-setup-additional-entropy-for-cloud-servers-using-haveged>`_
      provides a good overview of sources of randomness.

Here is an example of creating a key. Note that we provide a name for the key first
(which we can use to reference the key later) and an email address:

.. code-block:: console

    $ spack gpg create dinosaur dinosaur@thedinosaurthings.com


If you want to export the key as you create it:


.. code-block:: console

    $ spack gpg create --export key.pub dinosaur dinosaur@thedinosaurthings.com

Or the private key:


.. code-block:: console

    $ spack gpg create --export-secret key.priv dinosaur dinosaur@thedinosaurthings.com


You can include both ``--export`` and ``--export-secret``, each with
an output file of choice, to export both.


^^^^^^^^^^^^
Listing keys
^^^^^^^^^^^^

In order to list the keys available in the keyring, the
``spack gpg list`` command will list trusted keys with the ``--trusted`` flag
and keys available for signing using ``--signing``. If you would like to
remove keys from your keyring, use ``spack gpg untrust <keyid>``. Key IDs can be
email addresses, names, or (best) fingerprints. Here is an example of listing
the key that we just created:

.. code-block:: console

    gpgconf: socketdir is '/run/user/1000/gnupg'
    /home/spackuser/spack/opt/spack/gpg/pubring.kbx
    ----------------------------------------------------------
    pub   rsa4096 2021-03-25 [SC]
          60D2685DAB647AD4DB54125961E09BB6F2A0ADCB
    uid           [ultimate] dinosaur (GPG created for Spack) <dinosaur@thedinosaurthings.com>


Note that the name "dinosaur" can be seen under the uid, which is the unique
id. We might need this reference if we want to export or otherwise reference the key.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Signing and Verifying Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to sign a package, ``spack gpg sign <file>`` should be used. By
default, the signature will be written to ``<file>.asc``, but that may be
changed by using the ``--output <file>`` flag. If there is only one signing
key available, it will be used, but if there is more than one, the key to use
must be specified using the ``--key <keyid>`` flag. The ``--clearsign`` flag
may also be used to create a signed file which contains the contents, but it
is not recommended. Signed packages may be verified by using
``spack gpg verify <file>``.


^^^^^^^^^^^^^^
Exporting Keys
^^^^^^^^^^^^^^

You might want to export a public key, and that looks like this. Let's
use the previous example and ask Spack to export the key with uid "dinosaur."
We will provide an output location (typically a `*.pub` file) and the name of
the key.

.. code-block:: console

    $ spack gpg export dinosaur.pub dinosaur

You can then look at the created file, `dinosaur.pub`, to see the exported key.
If you want to include the private key, then just add `--secret`:

.. code-block:: console

    $ spack gpg export --secret dinosaur.priv dinosaur

This will write the private key to the file `dinosaur.priv`.

.. warning::

    You should be very careful about exporting private keys. You likely would
    only want to do this in the context of moving your Spack installation to
    a different server, and wanting to preserve keys for a build cache. If you
    are unsure about exporting, you can ask your local system administrator
    or for help on an issue or the Spack Slack.


.. _windows_support:

----------------
Spack On Windows
----------------

Windows support for Spack is currently under development. While this work is still in an early stage,
it is currently possible to set up Spack and perform a few operations on Windows.  This section will guide
you through the steps needed to install Spack and start running it on a fresh Windows machine.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 1: Install prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use Spack on Windows, you will need the following packages:

Required:
* Microsoft Visual Studio
* Python
* Git
* 7z

Optional:
* Intel Fortran (needed for some packages)

.. note::

  Currently MSVC is the only compiler tested for C/C++ projects. Intel OneAPI provides Fortran support.

"""""""""""""""""""""""
Microsoft Visual Studio
"""""""""""""""""""""""

Microsoft Visual Studio provides the only Windows C/C++ compiler that is currently supported by Spack.
Spack additionally requires that the Windows SDK (including WGL) to be installed as part of your
Visual Studio installation as it is required to build many packages from source.

We require several specific components to be included in the Visual Studio installation.
One is the C/C++ toolset, which can be selected as "Desktop development with C++" or "C++ build tools,"
depending on installation type (Professional, Build Tools, etc.)  The other required component is
"C++ CMake tools for Windows," which can be selected from among the optional packages.
This provides CMake and Ninja for use during Spack configuration.


If you already have Visual Studio installed, you can make sure these components are installed by
rerunning the installer.  Next to your installation, select "Modify" and look at the
"Installation details" pane on the right.

"""""""""""""
Intel Fortran
"""""""""""""

For Fortran-based packages on Windows, we strongly recommend Intel's oneAPI Fortran compilers.
The suite is free to download from Intel's website, located at
https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/fortran-compiler.html.
The executable of choice for Spack will be Intel's Beta Compiler, ifx, which supports the classic
compiler's (ifort's) frontend and runtime libraries by using LLVM.

""""""
Python
""""""

As Spack is a Python-based package, an installation of Python will be needed to run it.
Python 3 can be downloaded and installed from the Windows Store, and will be automatically added
to your ``PATH`` in this case.

.. note::
   Spack currently supports Python versions later than 3.2 inclusive.

""""""
Git
""""""

A bash console and GUI can be downloaded from https://git-scm.com/downloads.
If you are unfamiliar with Git, there are a myriad of resources online to help
guide you through checking out repositories and switching development branches.

When given the option of adjusting your ``PATH``, choose the ``Git from the
command line and also from 3rd-party software`` option. This will automatically
update your ``PATH`` variable to include the ``git`` command.

Spack support on Windows is currently dependent on installing the Git for Windows project
as the project providing Git support on Windows. This is additionally the recommended method
for installing Git on Windows, a link to which can be found above. Spack requires the
utilities vendored by this project.

""""""
7zip
""""""

A tool for extracting ``.xz`` files is required for extracting source tarballs. The latest 7-Zip
can be located at https://sourceforge.net/projects/sevenzip/.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 2: Install and setup Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are now ready to get the Spack environment set up on our machine. We
begin by using Git to clone the Spack repo, hosted at https://github.com/spack/spack.git
into a desired directory, for our purposes today, called ``spack_install``.

In order to install Spack with Windows support, run the following one-liner
in a Windows CMD prompt.

.. code-block:: console

   git clone https://github.com/spack/spack.git

.. note::
   If you chose to install Spack into a directory on Windows that is set up to require Administrative
   Privileges, Spack will require elevated privileges to run.
   Administrative Privileges can be denoted either by default, such as
   ``C:\Program Files``, or administrator-applied administrative restrictions
   on a directory that Spack installs files to such as ``C:\Users``

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 3: Run and configure Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Windows, Spack supports both primary native shells, Powershell and the traditional command prompt.
To use Spack, pick your favorite shell, and run ``bin\spack_cmd.bat`` or ``share/spack/setup-env.ps1``
(you may need to Run as Administrator) from the top-level Spack
directory. This will provide a Spack-enabled shell. If you receive a warning message that Python is not in your ``PATH``
(which may happen if you installed Python from the website and not the Windows Store), add the location
of the Python executable to your ``PATH`` now. You can permanently add Python to your ``PATH`` variable
by using the ``Edit the system environment variables`` utility in Windows Control Panel.

To configure Spack, first run the following command inside the Spack console:

.. code-block:: console

   spack compiler find

This creates a ``.staging`` directory in our Spack prefix, along with a ``windows`` subdirectory
containing a ``packages.yaml`` file. On a fresh Windows installation with the above packages
installed, this command should only detect Microsoft Visual Studio and the Intel Fortran
compiler will be integrated within the first version of MSVC present in the ``packages.yaml``
output.

Spack provides a default ``config.yaml`` file for Windows that it will use unless overridden.
This file is located at ``etc\spack\defaults\windows\config.yaml``. You can read more on how to
do this and write your own configuration files in the :ref:`Configuration Files<configuration>` section of our
documentation. If you do this, pay particular attention to the ``build_stage`` block of the file
as this specifies the directory that will temporarily hold the source code for the packages to
be installed. This path name must be sufficiently short for compliance with CMD, otherwise you
will see build errors during installation (particularly with CMake) tied to long path names.

To allow Spack's use of external tools and dependencies already on your system, the
external pieces of software must be described in the ``packages.yaml`` file.
There are two methods to populate this file:

The first and easiest choice is to use Spack to find installations on your system. In
the Spack terminal, run the following commands:

.. code-block:: console

   spack external find cmake
   spack external find ninja

The ``spack external find <name>`` will find executables on your system
with the same name given. The command will store the items found in
``packages.yaml`` in the ``.staging\`` directory.

Assuming that the command found CMake and Ninja executables in the previous
step, continue to Step 4. If no executables were found, we may need to manually direct Spack towards the CMake
and Ninja installations we set up with Visual Studio. Therefore, your ``packages.yaml`` file will look something
like this, possibly with slight variations in the paths to CMake and Ninja:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.19
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake'
       buildable: False
     ninja:
       externals:
       - spec: ninja@1.8.2
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'
       buildable: False

You can also use a separate installation of CMake if you have one and prefer
to use it. If you don't have a path to Ninja analogous to the above, then you can
obtain it by running the Visual Studio Installer and following the instructions
at the start of this section. Also note that YAML files use spaces for indentation
and not tabs, so ensure that this is the case when editing one directly.


.. note:: Cygwin
   The use of Cygwin is not officially supported by Spack and is not tested.
   However, Spack will not prevent this, so if choosing to use Spack
   with Cygwin, know that no functionality is guaranteed.

^^^^^^^^^^^^^^^^^
Step 4: Use Spack
^^^^^^^^^^^^^^^^^

Once the configuration is complete, it is time to give the installation a test.  Install a basic package through the
Spack console via:

.. code-block:: console

   spack install cpuinfo

If in the previous step, you did not have CMake or Ninja installed, running the command above should install both packages.

.. note:: Spec Syntax Caveats
   Windows has a few idiosyncrasies when it comes to the Spack spec syntax and the use of certain shells
   See the Spack spec syntax doc for more information


^^^^^^^^^^^^^^
For developers
^^^^^^^^^^^^^^

The intent is to provide a Windows installer that will automatically set up
Python, Git, and Spack, instead of requiring the user to do so manually.
Instructions for creating the installer are at
https://github.com/spack/spack/blob/develop/lib/spack/spack/cmd/installer/README.md
