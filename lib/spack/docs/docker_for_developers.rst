.. _docker_for_developers:

=====================
Docker for Developers
=====================

This guide is intended for people who want to use our prepared docker
environments to work on developing Spack or working on spack packages. It is
meant to serve as the companion documentation for the :ref:`packaging-guide`.

--------
Overview
--------

To get started, all you need is the latest version of ``docker`` and
``docker-compose``.

.. code-block:: console

    $ cd share/spack/docker
    $ docker-compose run --rm ubuntu

This command should drop you into an interactive shell where you can run spack
within an isolated docker container running ubuntu.  The copy of spack being
used should be tied to the working copy of your cloned git repo, so any changes
you make should be immediately reflected in the running docker container.  Feel
free to add or modify any packages or to hack on spack, itself.  Your contained
copy of spack should immediately reflect all changes.

To work within a container running a different linux distro, change the "ubuntu"
argument to any one of the services listed under the ``docker-compose.yml``
file.

.. code-block:: console

    $ docker-compose config --services
    fedora
    ubuntu
    $ docker-compose run --rm fedora
