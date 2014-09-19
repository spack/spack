Spack
===========

Spack is a package management tool designed to support multiple
versions and configurations of software on a wide variety of platforms
and environments. It was designed for large supercomputing centers,
where many users and application teams share common installations of
software on clusters with exotic architectures, using libraries that
do not have a standard ABI. Spack is non-destructive: installing a new
version does not break existing installations, so many configurations
can coexist on the same system.

Most importantly, Spack is simple. It offers a simple spec syntax so
that users can specify versions and configuration options
concisely. Spack is also simple for package authors: package files are
writtin in pure Python, and specs allow package authors to write a
single build script for many different builds of the same package.

See the
[Feature Overview](http://scalability-llnl.github.io/spack/features.html)
for examples and highlights.

To install spack and install your first package:

    $ git clone git@github.com:scalability-llnl/spack.git
    $ cd spack/bin
    $ ./spack install libelf

Documentation
----------------

[Full documentation](http://scalability-llnl.github.io/spack)
for Spack is also available.

Authors
----------------
Spack was written by Todd Gamblin, tgamblin@llnl.gov.

Significant contributions were also made by the following awesome
people:

  * David Beckingsale
  * David Boehme
  * Luc Jaulmes
  * Matt Legendre
  * Greg Lee
  * Adam Moody

Release
----------------
Spack is released under an LGPL license.  For more details see the
LICENSE file.

``LLNL-CODE-647188``
