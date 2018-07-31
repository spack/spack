# <img src="https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo.svg" width="64" valign="middle" alt="Spack"/> Spack

[![Build Status](https://travis-ci.org/spack/spack.svg?branch=develop)](https://travis-ci.org/spack/spack)
[![codecov](https://codecov.io/gh/spack/spack/branch/develop/graph/badge.svg)](https://codecov.io/gh/spack/spack)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://spack.readthedocs.io)
[![Slack](https://spackpm.herokuapp.com/badge.svg)](https://spackpm.herokuapp.com)

Spack is a multi-platform package manager that builds and installs
multiple versions and configurations of software. It works on Linux,
macOS, and many supercomputers. Spack is non-destructive: installing a
new version of a package does not break existing installations, so many
configurations of the same package can coexist.

Spack offers a simple "spec" syntax that allows users to specify versions
and configuration options. Package files are written in pure Python, and
specs allow package authors to write a single script for many different
builds of the same package.  With Spack, you can build your software
*all* the ways you want to.

See the
[Feature Overview](http://spack.readthedocs.io/en/latest/features.html)
for examples and highlights.

To install spack and your first package, make sure you have Python.
Then:

    $ git clone https://github.com/spack/spack.git
    $ cd spack/bin
    $ ./spack install libelf

Documentation
----------------

[**Full documentation**](http://spack.readthedocs.io/) for Spack is
the first place to look.

Try the
[**Spack Tutorial**](http://spack.readthedocs.io/en/latest/tutorial.html),
to learn how to use spack, write packages, or deploy packages for users
at your site.

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

If you are interested in contributing to spack, join the mailing list.
We're using Google Groups for this:

  * [Spack Google Group](https://groups.google.com/d/forum/spack)

### Slack channel

Spack has a Slack channel where you can chat about all things Spack:

  * [Spack on Slack](https://spackpm.slack.com)

[Sign up here](https://spackpm.herokuapp.com) to get an invitation mailed
to you.

### Twitter

You can follow [@spackpm](https://twitter.com/spackpm) on Twitter for
updates. Also, feel free to `@mention` us in in questions or comments
about your own experience with Spack.

### Contributions

Contributing to Spack is relatively easy.  Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/).
When you send your request, make ``develop`` the destination branch on the
[Spack repository](https://github.com/spack/spack).

Your PR must pass Spack's unit tests and documentation tests, and must be
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.  We enforce
these guidelines with [Travis CI](https://travis-ci.org/spack/spack).  To
run these tests locally, and for helpful tips on git, see our
[Contribution Guide](http://spack.readthedocs.io/en/latest/contribution_guide.html).

Spack uses a rough approximation of the
[Git Flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model.  The ``develop`` branch contains the latest
contributions, and ``master`` is always tagged and points to the latest
stable release.

Authors
----------------
Many thanks go to Spack's [contributors](https://github.com/spack/spack/graphs/contributors).

Spack was created by Todd Gamblin, tgamblin@llnl.gov.

### Citing Spack

If you are referencing Spack in a publication, please cite the following paper:

 * Todd Gamblin, Matthew P. LeGendre, Michael R. Collette, Gregory L. Lee,
   Adam Moody, Bronis R. de Supinski, and W. Scott Futral.
   [**The Spack Package Manager: Bringing Order to HPC Software Chaos**](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf).
   In *Supercomputing 2015 (SC’15)*, Austin, Texas, November 15-20 2015. LLNL-CONF-669890.

Release
----------------
Spack is released under an LGPL license.  For more details see the
NOTICE and LICENSE files.

``LLNL-CODE-647188``

![Analytics](https://ga-beacon.appspot.com/UA-101208306-3/welcome-page?pixel)
