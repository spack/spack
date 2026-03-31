..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      If you update an existing Spack instance, this section explains what to look out for.

Updating Spack
==============

If you have an existing instance of spack and you update it with ``git pull``, this should generally work fine.
Spack's behavior can differ between minor releases and this section explains what you might have to update.

The most-significant changes are documented in https://github.com/spack/spack/discussions/30634

1.2
---

Moving all data written by Spack out of the spack prefix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See: https://github.com/spack/spack/pull/47615

One of the most significant changes is where Spack will put (and look for) installed packages:

- If you don't clone a new instance of Spack, and only ``git pull`` into old instances, then each of those will continue to write into their own prefixes.
- If new instances are cloned but are configured to write outside of the default in ``~``, then old spack instances will continue to write into their own prefixes.
- If any new spack instance is cloned and writes into ``~`` (the new default in 1.2), then any old spack instance that updates to version 1.2 will start writing into ``~`` as well.

  - If you want to force an old instance to continue to write into the old default after pulling 1.2, then you will need to set ``config:install_tree:root`` to point to that location (``$spack/opt/spack``).
  - You can do this "ahead of time" as well: set ``config:install_tree:root`` before pulling 1.2.

Other data stored in ``$spack`` also moves out in 1.2:

- Environments, and you can restore old behavior with ``config:environments_root:$spack/var/spack/environments``.
- Modules, and you can restore old behavior by setting ``modules:default:roots:{tcl,lmod}`` to ``$spack/share/spack/{modules,lmod}``
- GPG keys

  - Default trusted keys for ``spack gpg init`` are stored in ``$spack/var/spack/gpg``.
    If mixing old and new instances of spack ``spack gpg init --from=<spack-prefix>/var/spack/gpg`` if you placed any keys there (in other words, that directory is managed like any external store of GPG keys).
  - You can use the old storage location for keys by setting the ``SPACK_GNUPGHOME`` environment variable to ``<spack-prefix>/opt/spack/gpg``.
