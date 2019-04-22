.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _spack-101:

=============================
Tutorial: Spack 101
=============================

This is a full-day introduction to Spack with lectures and live demos.
It was presented as a tutorial for staff at the `RIKEN Center for
Computational Science (R-CCS)
<http://www.riken.jp/en/research/labs/r-ccs/>`_.  You can use these
materials to teach a course on Spack at your own site, or you can just
skip ahead and read the live demo scripts to see how Spack is used in
practice.

.. _sc16-slides:

.. rubric:: Slides

.. figure:: tutorial/sc16-tutorial-slide-preview.png
   :target: https://spack.io/slides/Spack-RIKEN19-Tutorial.pdf
   :height: 72px
   :align: left
   :alt: Slide Preview

`Download Slides <https://spack.io/slides/Spack-RIKEN19-Tutorial.pdf>`_.

**Full citation:** Todd Gamblin, Gregory Becker, and Peter Scheibel.
Managing HPC Software Complexity with Spack.  Tutorial presented at RIKEN
Center for Computational Science. April 23, 2019.  Kobe, Japan.

.. _sc16-live-demos:

.. rubric:: Live Demos

We provide scripts that take you step-by-step through basic Spack tasks.
They correspond to sections in the slides above. You can use one of the
following methods to run through the scripts:

  1. We provide the `spack/tutorial
     <https://hub.docker.com/r/spack/tutorial>`_ container image on
     Docker Hub that you can use to do the tutorial on your local
     machine.  You can invoke ``docker run -it spack/tutorial`` to start
     using the container.

  2. When we host the tutorial, we also provision VM instances in `AWS
     <https://aws.amazon.com/>`_, so that users who are unfamiliar with
     Docker can simply log into a VPM to do the demo exercises.

You should now be ready to run through our demo scripts:

  1. :ref:`basics-tutorial`
  2. :ref:`configs-tutorial`
  3. :ref:`packaging-tutorial`
  4. :ref:`environments-tutorial`
  5. :ref:`modules-tutorial`
  6. :ref:`build-systems-tutorial`
  7. :ref:`advanced-packaging-tutorial`

Full contents:

.. toctree::
   tutorial_basics
   tutorial_configuration
   tutorial_packaging
   tutorial_environments
   tutorial_modules
   tutorial_buildsystems
   tutorial_advanced_packaging
