.. _intelpackage:

------------
IntelPackage
------------

Intel provides many licensed software packages, which all share the
same basic steps for configuring and installing, as well as license
management.

This build system is a work-in-progress. See
https://github.com/spack/spack/pull/4300 and
https://github.com/spack/spack/pull/7469 for more information.


Spack interacts with Intel packages in three ways: (1) as external tools, (2)
as tools to install within Spack, and (3) as tools to use to compile other
packages, also within Spack.


Integration of Intel packages *external* to Spack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A site that already uses Intel tools, especially licensed ones, will likely
have some versions already installed on the system, especially at a time when
Spack is just being introduced. It will be useful to make such previously
installed tools available for use by Spack as they are.

External Intel *compilers*, like all compilers that Spack is to use, are
configured in ``compilers.yaml`` files located in ``$SPACK_ROOT/etc/spack/`` or
the user's own ``~/.spack/`` directory. Specifics for the Intel compilers are
discussed at
http://spack.readthedocs.io/en/latest/getting_started.html#intel-compilers .

External *library-type* packages (as opposed to compilers) are configured for
Spack in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, as documented at
http://spack.readthedocs.io/en/latest/build_settings.html#external-packages .

These ``packages.yaml`` files resolve a Spack spec via either ``paths`` or
``modules`` tokens to specific pre-installed package versions on the system
that you wish to integrate.  Since Intel tools generally need environment
variables to interoperate, the ``modules`` token will be preferable.  Its
named modulefile, generated and managed outside of Spack's purview, will be
loaded when the corresponding spec is required.

The following exampleintegrates the packages activated by the external
``intel-mkl/18/18.0.1`` and ``intel-mkl/18/18.0.2`` modulefiles as Spack
packages ``intel-mkl@2018.1.163`` and ``intel-mkl@2018.2.199``, respectively:

.. code-block:: yaml

   packages:
     intel-mkl:
       modules:
         intel-mkl@2018.1.163  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.1
         intel-mkl@2018.2.199  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.2

If your system administrator did not provide modules for the Intel tools
available, you could do well to ask for them, because installing multiple
copies of the Intel tools is bound to stretch disk space and patience thin. If
you *are* the system administrator and are still new to modules, then perhaps
it's best to follow the next section and install the Intel tools solely within
Spack.

A more advanced version follows, illustrating how to provide variants
and using the ``buildable: False`` declaration to disallow Spack to install
packages through its normal internal mechanism.

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       modules:
         intel-parallel-studio@cluster.2018.1.163 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.1
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.2
       buildable: False


Installing within Spack
~~~~~~~~~~~~~~~~~~~~~~~

Installation of Intel compilers and libraries *within* Spack.

Compilers always require a license - see Section Licenses below.

...


Using within Spack
~~~~~~~~~~~~~~~~~~

Once Intel packages are integrated as external package or installed within
Spack, they can be used as intended for installing what we'll call *client
packages* within Spack.  There are actually three different routes for using
Intel packages:

* Compilers, as explicitly named the client spec.

    Needs editing ``compilers.yaml`` and always requires a license.
    ...

* Implicitly as virtual packages that satisfy a requirement for a library that
  is available in different flavors, namely BLAS, Lapack, and MPI.

  Intel packages can be selected either in the client package spec or by
  ``providers`` settings in ``packages.yaml``.
  ...

* As explicit dependency (DAAL, IPP – TBD).
  ...


Licenses
~~~~~~~~~

Some of Intel's software products require a license, in particular
the core development packages of compilers, analyzers, and optimizers.
These are available in Spack as:

* ``intel-parallel-studio`` - entire suite
* ``intel`` - compilers-only subset

Note that from 2017 onwards Intel made many of its performance libraries,
notably MPI and MKL, available for use without purchasing a license.

For packages that do require a license, it is needed not only during use, but
typically already at installation time.  If you plan on having Spack install
any such package, the Intel installer that Spack will run for you must be able
to find your license.

Therefore, *before* executing ``spack install intel-<pkg>``, provide the
license by one of the following means:


**License Server**

Setting up a license server as such is outside the scope of Spack. We assume
your system administrator has a license server running and has installed
network licenses for Intel packages.

To use an Intel license server client-side, i.e., by an Intel installer to
install licensed library packages or compilers, the client needs to find out or
be told the host name(s) and port number(s) of the license server, which can be
done by three methods, all described at
https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license .

Note, that ideally, your license administrator will *already have installed*
the necessary files to tell clients where to reach the server.

Notably, any files under ``/opt/intel/licenses/foo.lic`` that have the form::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

will be found automatically by client processess like installers and eventually
compilers and require no further action to use them.  While not particularly
recommended, even the actual network license files containing full PACKAGE and
INCREMENT data could be placed this way, as long as the ``USE_SERVER`` token is
present or has been added in the header.

Note that you can *install* a licensed product even when the actual FlexLM
server process is not running, by specifying the license server as ``export
INTEL_LICENSE_FILE=port@serverhost``.

...


**License File**

If you purchased a single-user license, obtain your license file as instructed
by Intel. You can request that the license file be re-sent to you `following
Intel's instructions
<https://software.intel.com/en-us/articles/resend-license-file>`_.

The license file is a plain text file. Install the file in one of the following
directories, creating them if necessary, and using either the downloaded name
or another suitably plain name that ends in ``.lic``:

1. ``/opt/intel/licenses/``. This is the preferred and default location. Use it
   if you have write access there.

2. Any other suitable directory you can write to, preferably used to hold
   licenses only.  A recommended user-specific location is: ``~/intel/licenses/``.

   Specify that directory and optionally the file name in an environment
   variable ``export INTEL_LICENSE_FILE="/path/to/downloaded_name.lic"``.

The Intel installer will search both the default directory and the contents of
the environment variable ``INTEL_LICENSE_FILE``.  Despite its name, this is
actually a PATH style variable that can hold a list drectories (optionally with
file names), all separated by ":" (on Linux and Mac). The installer will try
all ``*.lic`` files named or reachable in the given directories.

For more, see:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses

...
