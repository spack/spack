.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _monitoring:

==========
Monitoring
==========

You can use a `spack monitor <https://github.com/spack/spack-monitor>`_ "Spackmon"
server to store a database of your packages, builds, and associated metadata 
for provenance, research, or some other kind of development. You should
follow the instructions in the `spack monitor documentation <https://spack-monitor.readthedocs.org>`_
to first create a server along with a username and token for yourself.
You can then use this guide to interact with the server.

-------------------
Analysis Monitoring
-------------------

To read about how to monitor an analysis (meaning you want to send analysis results
to a server) see :ref:`analyze_monitoring`.

---------------------
Monitoring An Install
---------------------

Since an install is typically when you build packages, we logically want
to tell spack to monitor during this step. Let's start with an example
where we want to monitor the install of hdf5. Unless you have disabled authentication
for the server, we first want to export our spack monitor token and username to the environment:

.. code-block:: console
 
    $ export SPACKMON_TOKEN=50445263afd8f67e59bd79bff597836ee6c05438
    $ export SPACKMON_USER=spacky


By default, the host for your server is expected to be at ``http://127.0.0.1``
with a prefix of ``ms1``, and if this is the case, you can simply add the
``--monitor`` flag to the install command:

.. code-block:: console

    $ spack install --monitor hdf5


If you need to customize the host or the prefix, you can do that as well:

.. code-block:: console

    $ spack install --monitor --monitor-prefix monitor --monitor-host https://monitor-service.io hdf5


As a precaution, we cut out early in the spack client if you have not provided
authentication credentials. For example, if you run the command above without
exporting your username or token, you'll see:

.. code-block:: console

    ==> Error: You are required to export SPACKMON_TOKEN and SPACKMON_USER

This extra check is to ensure that we don't start any builds,
and then discover that you forgot to export your token. However, if 
your monitoring server has authentication disabled, you can tell this to
the client to skip this step:

.. code-block:: console

    $ spack install --monitor --monitor-disable-auth hdf5

If the service is not running, you'll cleanly exit early - the install will
not continue if you've asked it to monitor and there is no service.
For example, here is what you'll see if the monitoring service is not running:

.. code-block:: console

    [Errno 111] Connection refused


If you want to continue builds (and stop monitoring) you can set the ``--monitor-keep-going``
flag. 

.. code-block:: console

    $ spack install --monitor --monitor-keep-going hdf5

This could mean that if a request fails, you only have partial or no data
added to your monitoring database. This setting will not be applied to the
first request to check if the server is running, but to subsequent requests.
If you don't have a monitor server running and you want to build, simply
don't provide the ``--monitor`` flag! Finally, if you want to provide one or
more tags to your build, you can do:

.. code-block:: console

    # Add one tag, "pizza"
    $ spack install --monitor --monitor-tags pizza hdf5

    # Add two tags, "pizza" and "pasta"
    $ spack install --monitor --monitor-tags pizza,pasta hdf5


----------------------------
Monitoring with Containerize
----------------------------

The same argument group is available to add to a containerize command. 

^^^^^^
Docker
^^^^^^

To add monitoring to a Docker container recipe generation using the defaults,
and assuming a monitor server running on localhost, you would
start with a spack.yaml in your present working directory:

.. code-block:: yaml

   spack:
     specs:
       - samtools

And then do:

.. code-block:: console

    # preview first
    spack containerize --monitor
    
    # and then write to a Dockerfile
    spack containerize --monitor > Dockerfile
    
    
The install command will be edited to include commands for enabling monitoring.
However, getting secrets into the container for your monitor server is something
that should be done carefully. Specifically you should:

 - Never try to define secrets as ENV, ARG, or using ``--build-arg``
 - Do not try to get the secret into the container via a "temporary" file that you remove (it in fact will still exist in a layer)

Instead, it's recommended to use buildkit `as explained here <https://pythonspeed.com/articles/docker-build-secrets/>`_.
You'll need to again export environment variables for your spack monitor server:

.. code-block:: console

    $ export SPACKMON_TOKEN=50445263afd8f67e59bd79bff597836ee6c05438
    $ export SPACKMON_USER=spacky

And then use buildkit along with your build and identifying the name of the secret:

.. code-block:: console

    $ DOCKER_BUILDKIT=1 docker build --secret id=st,env=SPACKMON_TOKEN --secret id=su,env=SPACKMON_USER -t spack/container . 
    
The secrets are expected to come from your environment, and then will be temporarily mounted and available
at ``/run/secrets/<name>``. If you forget to supply them (and authentication is required) the build
will fail. If you need to build on your host (and interact with a spack monitor at localhost) you'll
need to tell Docker to use the host network:

.. code-block:: console

    $ DOCKER_BUILDKIT=1 docker build --network="host" --secret id=st,env=SPACKMON_TOKEN --secret id=su,env=SPACKMON_USER -t spack/container . 
    

^^^^^^^^^^^
Singularity
^^^^^^^^^^^

To add monitoring to a Singularity container build, the spack.yaml needs to
be modified slightly to specify wanting a different format:


.. code-block:: yaml

   spack:
     specs:
       - samtools
     container:
       format: singularity
       
       
Again, generate the recipe:


.. code-block:: console

    # preview first
    $ spack containerize --monitor
    
    # then write to a Singularity recipe
    $ spack containerize --monitor > Singularity


Singularity doesn't have a direct way to define secrets at build time, so we have
to do a bit of a manual command to add a file, source secrets in it, and remove it.
Since Singularity doesn't have layers like Docker, deleting a file will truly
remove it from the container and history. So let's say we have this file,
``secrets.sh``:

.. code-block:: console

    # secrets.sh
    export SPACKMON_USER=spack
    export SPACKMON_TOKEN=50445263afd8f67e59bd79bff597836ee6c05438


We would then generate the Singularity recipe, and add a files section,
a source of that file at the start of ``%post``, and **importantly**
a removal of the final at the end of that same section.

.. code-block::

    Bootstrap: docker
    From: spack/ubuntu-bionic:latest
    Stage: build

    %files
      secrets.sh /opt/secrets.sh 

    %post
      . /opt/secrets.sh

      # spack install commands are here
      ...
      
      # Don't forget to remove here!
      rm /opt/secrets.sh


You can then build the container as your normally would.

.. code-block:: console

    $ sudo singularity build container.sif Singularity 


------------------
Monitoring Offline
------------------

In the case that you want to save monitor results to your filesystem
and then upload them later (perhaps you are in an environment where you don't
have credentials or it isn't safe to use them) you can use the ``--monitor-save-local``
flag.

.. code-block:: console

    $ spack install --monitor --monitor-save-local hdf5 

This will save results in a subfolder, "monitor" in your designated spack
reports folder, which defaults to ``$HOME/.spack/reports/monitor``. When
you are ready to upload them to a spack monitor server:


.. code-block:: console

    $ spack monitor upload ~/.spack/reports/monitor 


You can choose the root directory of results as shown above, or a specific
subdirectory. The command accepts other arguments to specify configuration
for the monitor.
