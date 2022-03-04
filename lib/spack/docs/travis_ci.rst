.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

========================
Using Spack on Travis-CI
========================

Spack can be deployed as a provider for userland software in
`Travis-CI <https://http://travis-ci.org>`_.

A starting-point for a ``.travis.yml`` file can look as follows.
It uses `caching <https://docs.travis-ci.com/user/caching/>`_ for
already built environments, so make sure to clean the Travis cache if
you run into problems.

The main points that are implemented below:

#. Travis is detected as having up to 34 cores available, but only 2
   are actually allocated for the user. We limit the parallelism of
   the spack builds in the config.
   (The Travis yaml parser is a bit buggy on the echo command.)

#. Without control for the user, Travis jobs will run on various
   ``x86_64`` microarchitectures. If you plan to cache build results,
   e.g. to accelerate dependency builds, consider building for the
   generic ``x86_64`` target only.
   Limiting the microarchitecture will also find more packages when
   working with the
   `E4S Spack build cache <https://oaciss.uoregon.edu/e4s/e4s_buildcache_inventory.html>`_.

#. Builds over 10 minutes need to be prefixed with ``travis_wait``.
   Alternatively, generate output once with ``spack install -v``.

#. Travis builds are non-interactive. This prevents using bash
   aliases and functions for modules. We fix that by sourcing
   ``/etc/profile`` first (or running everything in a subshell with
   ``bash -l -c '...'``).

.. code-block:: yaml

   language: cpp
   sudo: false
   dist: trusty

   cache:
     apt: true
     directories:
       - $HOME/.cache

   addons:
     apt:
       sources:
         - ubuntu-toolchain-r-test
       packages:
         - g++-4.9
         - environment-modules

   env:
     global:
       - SPACK_ROOT: $HOME/.cache/spack
       - PATH: $PATH:$HOME/.cache/spack/bin

   before_install:
     - export CXX=g++-4.9
     - export CC=gcc-4.9
     - export FC=gfortran-4.9
     - export CXXFLAGS="-std=c++11"

   install:
     - |
       if ! which spack >/dev/null; then
         mkdir -p $SPACK_ROOT &&
         git clone --depth 50 https://github.com/spack/spack.git $SPACK_ROOT &&
         printf "config:\n  build_jobs: 2\n" > $SPACK_ROOT/etc/spack/config.yaml &&
         printf "packages:\n  all:\n    target: ['x86_64']\n" \
                 > $SPACK_ROOT/etc/spack/packages.yaml;
       fi
     - travis_wait spack install cmake@3.7.2~openssl~ncurses
     - travis_wait spack install boost@1.62.0~graph~iostream~locale~log~wave
     - spack clean -a
     - source /etc/profile &&
       source $SPACK_ROOT/share/spack/setup-env.sh
     - spack load cmake
     - spack load boost

   script:
     - mkdir -p $HOME/build
     - cd $HOME/build
     - cmake $TRAVIS_BUILD_DIR
     - make -j 2
     - make test

