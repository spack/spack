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


Intel packages can be used by Spack in two ways:

1. Integration of packages that were installed on the system external to Spack.

2. New installation, all within Spack.


Licenses
~~~~~~~~~

Some of Intel's software products require a license, in particular
the core development packages of compilers, analyzers, and optimizers.
These are available in Spack as:

* ``intel-parallel-studio`` - entire suite
* ``intel`` - compilers-only subset

Fortunately, from 2017 onwards Intel made many of its performance libraries,
notably MPI and MKL, available for use without purchasing a license.

For packages that do require a license, it is needed not only during use, but
already at installation time.  If you plan on having Spack install any such
package, the Intel installer that Spack will run for you must be able to find
your license.

**Before** executing ``spack install intel-<pkg>``, provide the license by one
of the following means:

**License Server**
... what should users do to coordinate the license server with ``spack`` for installing the compiler suite? ...

**License File**
If you are using a single-user license you can obtain a license file from Intel
by logging in and `following Intel's instructions
<https://software.intel.com/en-us/articles/resend-license-file>`_.  With
``downloaded_name.lic`` downloaded on your local machine, you may either

1. Create the directory ``/opt/intel/licenses`` and copy ``downloaded_name.lic`` there (the Intel installer will search here by default).

2. Set the environment variable ``export INTEL_LICENSE_FILE="/path/to/downloaded_name.lic"``.

