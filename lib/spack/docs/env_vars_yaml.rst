.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _env-vars-yaml:

=============================================
Environment Variable Settings (env_vars.yaml)
=============================================

Spack allows you to include shell environment variable modifications
for a Spack environment by including an ``env_vars.yaml`` file. Environment
variables can be modified by setting, unsetting, appending, and prepending
variables in the shell environment.
The changes to the shell environment will take effect when the Spack
environment is activated.

For example:

.. code-block:: yaml

  env_vars:
    set:
      ENVAR_TO_SET_IN_ENV_LOAD: "FOO"
    unset:
      ENVAR_TO_UNSET_IN_ENV_LOAD:
    prepend_path:
      PATH_LIST: "path/to/prepend"
    append_path:
      PATH_LIST: "path/to/append"
    remove_path:
      PATH_LIST: "path/to/remove"


