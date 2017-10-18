Using this docker container for development.
------------

    $ cd share/spack/docker
    $ docker-compose run --rm ubuntu

This command should drop you into an interactive shell where you can run spack
within an isolated docker container running ubuntu.  The copy of spack being
used should be tied to the working copy of your cloned git repo, so any changes
you make should be immediately reflected in the running docker container.

To work within a container running a different linux distro, change the "ubuntu"
argument to any one of the services listed under the ``docker-compose.yml``
file.

    $ docker-compose config --services
    fedora
    ubuntu
    $ docker-compose run --rm fedora

