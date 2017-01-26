![image](share/spack/logo/spack-logo-text-64.png "Spack")
============

[![Build Status](https://travis-ci.org/LLNL/spack.svg?branch=develop)](https://travis-ci.org/LLNL/spack)
[![codecov](https://codecov.io/gh/LLNL/spack/branch/develop/graph/badge.svg)](https://codecov.io/gh/LLNL/spack)

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
written in pure Python, and specs allow package authors to write a
single build script for many different builds of the same package.

See the
[Feature Overview](http://spack.readthedocs.io/en/latest/features.html)
for examples and highlights.

To install spack and install your first package:

    $ git clone https://github.com/llnl/spack.git
    $ cd spack/bin
    $ ./spack install libelf

Documentation
----------------

[**Full documentation**](http://spack.readthedocs.io/) for Spack is
the first place to look.

We've also got a [**Spack 101 Tutorial**](http://spack.readthedocs.io/en/latest/tutorial_sc16.html),
so you can learn Spack yourself, or teach users at your own site.

See also:
  * [Technical paper](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf) and
    [slides](https://tgamblin.github.io/files/Gamblin-Spack-SC15-Talk.pdf) on Spack's design and implementation.
  * [Short presentation](https://tgamblin.github.io/files/Gamblin-Spack-Lightning-Talk-BOF-SC15.pdf) from the *Getting Scientific Software Installed* BOF session at Supercomputing 2015.


Get Involved!
------------------------

Spack is an open source project.  Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, or even new core features.

### Mailing list

If you are interested in contributing to spack, the first step is to
join the mailing list.  We're using a Google Group for this, and you
can join it here:

  * [Spack Google Group](https://groups.google.com/d/forum/spack)

### Contributions

Contributing to Spack is relatively easy.  Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/).
When you send your request, make ``develop`` the destination branch on the
[Spack repository](https://github.com/LLNL/spack).

Your PR must pass Spack's unit tests and documentation tests, and must be
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.
We enforce these guidelines with [Travis CI](https://travis-ci.org/LLNL/spack).
To run these tests locally, and for helpful tips on git, see our
[Contribution Guide](http://spack.readthedocs.io/en/latest/contribution_guide.html).

Spack uses a rough approximation of the [Git
Flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model.  The ``develop`` branch contains the latest
contributions, and ``master`` is always tagged and points to the
latest stable release.


Authors
----------------
Many thanks go to Spack's [contributors](https://github.com/llnl/spack/graphs/contributors).

Spack was originally written by Todd Gamblin, tgamblin@llnl.gov.

### Citing Spack

If you are referencing Spack in a publication, please cite the following paper:

 * Todd Gamblin, Matthew P. LeGendre, Michael R. Collette, Gregory L. Lee,
   Adam Moody, Bronis R. de Supinski, and W. Scott Futral.
   [**The Spack Package Manager: Bringing Order to HPC Software Chaos**](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf).
   In *Supercomputing 2015 (SC’15)*, Austin, Texas, November 15-20 2015. LLNL-CONF-669890.

Release
----------------
Spack is released under an LGPL license.  For more details see the
LICENSE file.

``LLNL-CODE-647188``
