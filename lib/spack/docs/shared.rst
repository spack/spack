.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. shared:

========================
Sharing a Spack Instance
========================

A single spack instance can be shared between users on a single system. Using this features allows environments and packages to be available to all users, but user installed packages and specs are not visible to anyone else. Additionally, packages installed a system level are protected from being uninstalled by other users. Changes made by any user will not impact any other user. 

------------
spack shared
------------
Interact with spack's shared mode.

.. code-block:: console

  spack shared [-h] SUBCOMMAND


Optional Arguments
| ``[-h, --help]`` shows help message

Subcommands:
  * activate
  * deactivate
  * status


| ``spack shared activate``
| Activates shared mode. When in shared mode, spack will default to installing packages to a user's specified path. Packages installed in this manner will be visible only to the user who installed the pacakge.

| ``spack shared deactivate``
| Deactivates shared mode. When in shared mode, spack will default to installing packages to the entire spack instance. Packages installed in this manner will be visible to all users.

| ``spack shared status``
| Displays whether shared mode is enabled or disabled.

------------------------
Configuring Shared Spack
------------------------

Shared spack uses a ``$SPACK_PATH`` environment variable to determine where to install user installed packages. Users can set their own path via ``export SPACK_PATH=/desired/spack/path`` otherwise spack defaults to using ``~/.spack``


-------------------
Using Shared Spack
-------------------
System administrators who are installing a shared instance of spack should install spack like ususal to their desired directory. When environments, mirrors, repos, etc. are configured properly, run ``spack shared activate`` to set the instance to a shared mode. Once enabled, spack will install packages to a user defined location and will prevent users from installing packages installed at the instance level. 

Users should configure their environment variable as demonstrated above. 
