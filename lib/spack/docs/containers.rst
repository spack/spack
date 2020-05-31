.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _containers:

================
Container Images
================

Spack can be an ideal tool to setup images for containers since all the
features discussed in :ref:`environments` can greatly help to manage
the installation of software during the image build process. Nonetheless,
building a production image from scratch still requires a lot of
boilerplate to:

- Get Spack working within the image, possibly running as root
- Minimize the physical size of the software installed
- Properly update the system software in the base image

To facilitate users with these tedious tasks, Spack provides a command
to automatically generate recipes for container images based on
Environments:

.. code-block:: console

   $ ls
   spack.yaml

   $ spack containerize
   # Build stage with Spack pre-installed and ready to be used
   FROM spack/centos7:latest as builder

   # What we want to install and how we want to install it
   # is specified in a manifest file (spack.yaml)
   RUN mkdir /opt/spack-environment \
   &&  (echo "spack:" \
   &&   echo "  specs:" \
   &&   echo "  - gromacs+mpi" \
   &&   echo "  - mpich" \
   &&   echo "  concretization: together" \
   &&   echo "  config:" \
   &&   echo "    install_tree: /opt/software" \
   &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

   # Install the software, remove unnecessary deps
   RUN cd /opt/spack-environment && spack install && spack gc -y

   # Strip all the binaries
   RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
       xargs file -i | \
       grep 'charset=binary' | \
       grep 'x-executable\|x-archive\|x-sharedlib' | \
       awk -F: '{print $1}' | xargs strip -s

   # Modifications to the environment that are necessary to run
   RUN cd /opt/spack-environment && \
       spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh


   # Bare OS image to run the installed executables
   FROM centos:7

   COPY --from=builder /opt/spack-environment /opt/spack-environment
   COPY --from=builder /opt/software /opt/software
   COPY --from=builder /opt/view /opt/view
   COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

   RUN yum update -y && yum install -y epel-release && yum update -y                                   \
    && yum install -y libgomp \
    && rm -rf /var/cache/yum  && yum clean all

   RUN echo 'export PS1="\[$(tput bold)\]\[$(tput setaf 1)\][gromacs]\[$(tput setaf 2)\]\u\[$(tput sgr0)\]:\w $ \[$(tput sgr0)\]"' >> ~/.bashrc


   LABEL "app"="gromacs"
   LABEL "mpi"="mpich"

   ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]


The bits that make this automation possible are discussed in details
below. All the images generated in this way will be based on
multi-stage builds with:

- A fat ``build`` stage containing common build tools and Spack itself
- A minimal ``final`` stage containing only the software requested by the user

-----------------
Spack Base Images
-----------------

Docker images with Spack preinstalled and ready to be used are
built on `Docker Hub <https://hub.docker.com/u/spack>`_
at every push to ``develop`` or to a release branch. The OS that
are currently supported are summarized in the table below:

.. _containers-supported-os:

.. list-table:: Supported operating systems
   :header-rows: 1

   * - Operating System
     - Base Image
     - Spack Image
   * - Ubuntu 16.04
     - ``ubuntu:16.04``
     - ``spack/ubuntu-xenial``
   * - Ubuntu 18.04
     - ``ubuntu:18.04``
     - ``spack/ubuntu-bionic``
   * - CentOS 6
     - ``centos:6``
     - ``spack/centos6``
   * - CentOS 7
     - ``centos:7``
     - ``spack/centos7``

All the images are tagged with the corresponding release of Spack:

.. image:: dockerhub_spack.png

with the exception of the ``latest`` tag that points to the HEAD
of the ``develop`` branch. These images are available for anyone
to use and take care of all the repetitive tasks that are necessary
to setup Spack within a container. All the container recipes generated
automatically by Spack use them as base images for their ``build`` stage.


-------------------------
Environment Configuration
-------------------------

Any Spack Environment can be used for the automatic generation of container
recipes. Sensible defaults are provided for things like the base image or the
version of Spack used in the image. If a finer tuning is needed it can be
obtained by adding the relevant metadata under the ``container`` attribute
of environments:

.. code-block:: yaml

   spack:
     specs:
     - gromacs+mpi
     - mpich

     container:
       # Select the format of the recipe e.g. docker,
       # singularity or anything else that is currently supported
       format: docker

       # Select from a valid list of images
       base:
         image: "centos:7"
         spack: develop

       # Whether or not to strip binaries
       strip: true

       # Additional system packages that are needed at runtime
       os_packages:
       - libgomp

       # Extra instructions
       extra_instructions:
         final: |
   RUN echo 'export PS1="\[$(tput bold)\]\[$(tput setaf 1)\][gromacs]\[$(tput setaf 2)\]\u\[$(tput sgr0)\]:\w $ \[$(tput sgr0)\]"' >> ~/.bashrc

       # Labels for the image
       labels:
         app: "gromacs"
         mpi: "mpich"

The tables below describe the configuration options that are currently supported:

.. list-table:: General configuration options for the ``container`` section of ``spack.yaml``
   :header-rows: 1

   * - Option Name
     - Description
     - Allowed Values
     - Required
   * - ``format``
     - The format of the recipe
     - ``docker`` or ``singularity``
     - Yes
   * - ``base:image``
     - Base image for ``final`` stage
     - See :ref:`containers-supported-os`
     - Yes
   * - ``base:spack``
     - Version of Spack
     - Valid tags for ``base:image``
     - Yes
   * - ``strip``
     - Whether to strip binaries
     - ``true`` (default) or ``false``
     - No
   * - ``os_packages``
     - System packages to be installed
     - Valid packages for the ``final`` OS
     - No
   * - ``extra_instructions:build``
     - Extra instructions (e.g. `RUN`, `COPY`, etc.) at the end of the ``build`` stage
     - Anything understood by the current ``format``
     - No
   * - ``extra_instructions:final``
     - Extra instructions (e.g. `RUN`, `COPY`, etc.) at the end of the ``final`` stage
     - Anything understood by the current ``format``
     - No
   * - ``labels``
     - Labels to tag the image
     - Pairs of key-value strings
     - No

.. list-table:: Configuration options specific to Singularity
   :header-rows: 1

   * - Option Name
     - Description
     - Allowed Values
     - Required
   * - ``singularity:runscript``
     - Content of ``%runscript``
     - Any valid script
     - No
   * - ``singularity:startscript``
     - Content of ``%startscript``
     - Any valid script
     - No
   * - ``singularity:test``
     - Content of ``%test``
     - Any valid script
     - No
   * - ``singularity:help``
     - Description of the image
     - Description string
     - No

Once the Environment is properly configured a recipe for a container
image can be printed to standard output by issuing the following
command from the directory where the ``spack.yaml`` resides:

.. code-block:: console

   $ spack containerize

The example ``spack.yaml`` above would produce for instance the
following ``Dockerfile``:

.. code-block:: docker

   # Build stage with Spack pre-installed and ready to be used
   FROM spack/centos7:latest as builder

   # What we want to install and how we want to install it
   # is specified in a manifest file (spack.yaml)
   RUN mkdir /opt/spack-environment \
   &&  (echo "spack:" \
   &&   echo "  specs:" \
   &&   echo "  - gromacs+mpi" \
   &&   echo "  - mpich" \
   &&   echo "  concretization: together" \
   &&   echo "  config:" \
   &&   echo "    install_tree: /opt/software" \
   &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

   # Install the software, remove unnecessary deps
   RUN cd /opt/spack-environment && spack install && spack gc -y

   # Strip all the binaries
   RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
       xargs file -i | \
       grep 'charset=binary' | \
       grep 'x-executable\|x-archive\|x-sharedlib' | \
       awk -F: '{print $1}' | xargs strip -s

   # Modifications to the environment that are necessary to run
   RUN cd /opt/spack-environment && \
       spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh


   # Bare OS image to run the installed executables
   FROM centos:7

   COPY --from=builder /opt/spack-environment /opt/spack-environment
   COPY --from=builder /opt/software /opt/software
   COPY --from=builder /opt/view /opt/view
   COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

   RUN yum update -y && yum install -y epel-release && yum update -y                                   \
    && yum install -y libgomp \
    && rm -rf /var/cache/yum  && yum clean all

   RUN echo 'export PS1="\[$(tput bold)\]\[$(tput setaf 1)\][gromacs]\[$(tput setaf 2)\]\u\[$(tput sgr0)\]:\w $ \[$(tput sgr0)\]"' >> ~/.bashrc


   LABEL "app"="gromacs"
   LABEL "mpi"="mpich"

   ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]

.. note::
   Spack can also produce Singularity definition files to build the image. The
   minimum version of Singularity required to build a SIF (Singularity Image Format)
   from them is ``3.5.3``.
