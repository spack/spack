.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      This is a guide for people who review package pull requests and includes criteria for them to be merged into the develop branch.

.. _package-review-guide:

Package Review Guide
====================

Package reviews are performed with the goals of minimizing build errors and making packages as **uniform and stable** as possible.

This section establishes guidelines to help reviewers assess and merge pull requests (PRs) to Spack’s community `package repository <https://github.com/spack/spack-packages>`_.
It describes the considerations and actions to be taken when reviewing new and updated `Spack packages <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#structure-of-a-package>`_.

Inappropriate Package
---------------------

It is rare that a package would be considered inappropriate for inclusion in the public `Spack package <https://github.com/spack/spack-packages>`_ repository.
One exception is making packages for standard Perl modules.

**Action.**
Should you find the software is not appropriate, explain to the :ref:`Package Contributor <package-contributors>` in a comment or your review.
Ask that the package be removed from the PR if it is one of multiple affected files; otherwise suggest the PR be closed.
In both cases, explain the reason for the request.

CORE Perl Modules
~~~~~~~~~~~~~~~~~

In general, modules that are part of the standard installation for all listed Perl versions (i.e., ``CORE``) should *not* be implemented or contributed as Spack packages.
Details on the exceptions and process for checking Perl modules can be found in the `Perl <https://spack.readthedocs.io/en/latest/build_systems/perlpackage.html#suitable_perl_modules>`_ build system documentation.

url, url_for_version, or URL Equivalent
---------------------------------------

Changes to URLs may invalidate existing versions, which should be checked when there is a URL-related modification.
All packages have a URL, though for some `build systems <https://spack.readthedocs.io/en/latest/build_systems.html>`_ it is derived automatically and not visible in the package.

Reasons `versions <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#versions-and-urls>`_ may become invalid include:

* the new URL does not support Spack version extrapolation;
* the addition of or changes to ``url_for_version`` involve checks of the ``spec``'s version instead of the ``version`` argument or the (usually older) versions are not covered;
* extrapolation of the derived URL no longer matches that of older versions; and
* the older versions are no longer available.

**Action.**
Checking existing version directives with checksums can usually be done manually with the modified package using `spack checksum <https://spack.readthedocs.io/en/latest/command_index.html#spack-checksum>`_.

**Solutions.**
Options for resolving the problem that can be suggested for investigation depend on the source.

In simpler cases involving ``url`` or ``url_for_version``, invalid versions can sometimes be corrected by ensuring all versions are covered by ``url_for_version``.
Alternatively, especially for older versions, the version-specific URL can be added as an argument to the ``version`` directive.

Sometimes the derived URLs of versions on the hosting system can vary.
This commonly happens with Python packages.
For example, the case of one or more letters in the package name may change at some point (e.g., `py-sphinx <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/py_sphinx/package.py>`_).
Also, dashes may be replaced with underscores (e.g., `py-scitkit-build <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/py_scikit_build/package.py>`_).
In some cases, both changes can occur for the same package.
As these examples illlustrate, it is sometimes possible to add a ``url_for_version`` method to override the default derived URL to ensure the correct one is returned.

If older versions are no longer available and there is a chance someone has the package in a build cache, the usual approach is to first suggest `deprecating <https://spack.readthedocs.io/en/latest/packaging_guide.html#deprecating-old-versions>`_ them in the package.

Maintainers Directive
----------------------

**Action.**
If the new package does not have a `maintainers <https://spack.readthedocs.io/en/latest/packaging_guide.html#maintainers>`_ directive, ask the :ref:`Package Contributor <package-contributors>` to consider adding themselves.

This request is optional for existing packages.

.. tip::

   Be prepared for them to refuse.

License Directive
-----------------

**Action.**
If the new package does not have a `license <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#license-information>`_  directive, ask the :ref:`Package Contributor <package-contributors>` to investigate and add it.

This request is optional for existing packages.

Version Directives
------------------

In general, Spack packages are expected to be built from source code.
There are a few exceptions (e.g., `BundlePackage <https://spack.readthedocs.io/en/latest/build_systems/bundlepackage.html#bundlepackage>`_).
Typically every package will have at least one `version directive <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#source-code-and-versions>`_.

**Action.**
The goal of reviewing this information is to confirm the existence and correctness of updated and new versions **and** that the versions are listed in descending order from newest to oldest.
The process for correctness checking depends on the arguments and nature of the software's downloads (see below).
Additions and removals of version directives should generally trigger a review of :ref:`dependencies <depends_on_reviews>`.

Checksums, commits, tags, and branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Checksums, commits, and tags.
  Normally these version arguments are automatically validated by GitHub Actions using `spack ci verify-versions <https://spack.readthedocs.io/en/latest/command_index.html#spack-ci-verify-versions>`_.

  **Action.**
  Review the PR's ``verify-checksums`` precheck to confirm.
  If necessary, checksums can usually be manually confirmed using `spack checksum <https://spack.readthedocs.io/en/latest/command_index.html#spack-checksum>`_.

  .. warning::

     From a security and reproducibility standpoint, it is important that Spack be able to verify downloaded source.
     This is accomplished using a hash (e.g., checksum or commit).
     See `checksum verification <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#checksum-verification>`_ for more information.

     Exceptions are allowed in rare cases, such as software supplied from reputable vendors.
     When in doubt, ask others with merge privileges for advice.

Tags.
  If a ``tag`` is provided without a ``commit``, the downloaded software will not be trusted.

  **Action.**
  Suggest that the ``commit`` argument be included in the ``version`` directive.

Branches.
  Confirming branches involves checking that they exist in the repository *and* that the version and branch names are consistent.

  **Action.**
  Confirming branch existence, on the other hand, often involves checking the source repository.

  In general, the version and branch names should match.
  When they do not, it is sometimes the result of people not being aware of how Spack handles `version ordering <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#version-comparison>`_.

  **Action.**
  If there is a name mismatch, especially for the most common branch names (e.g., `develop`, `main`, and `master`), ask why and suggest the arguments be changed such that they match the actual branch name.

Manual downloads.
  Edge cases, such as manually downloaded software, may be difficult to confirm.

  **Action.**
  In these cases it is acceptable to rely on the package's Maintainers, if any.

Deprecating Versions
~~~~~~~~~~~~~~~~~~~~

If someone is deprecating versions, it is good to find out why.
Sometimes there are concerns, such as security or lack of availability.

**Action.**
Suggest the Package Contributor review the `deprecation guidelines <https://spack.readthedocs.io/en/latest/packaging_guide.html#deprecating-old-versions>`_ before finalizing the changes if they haven't already explained why they made the choice in the PR description or comments.

Variant Directives
------------------

`Variants <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#variants>`_ represent build options so any changes involving these directives should be reflected elsewhere in the package.

Adding or Modifying Variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Action.**
Confirm that new or modified variants are actually used in the package.
The most common uses are additions and changes to:

* dependencies;
* configure options; and/or
* build arguments.

Removing or Disabling Variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the variant is still relevant to listed version directives, it may be preferable to adjust or add `conditions <https://spack.readthedocs.io/en/latest/packaging_guide.html#conditional-variants>`_.

**Action.**
Consider asking why the variant (or build option) is being removed and suggest making it conditional when it is still relevant.

.. warning::

    If the default value of a variant is changed in the PR, then there is a risk that other packages relying on that value will no longer build as others expect.
    This may be something worth noting in the review.

.. _depends_on_reviews:

Depends_on Directives
---------------------

`Dependencies <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#dependencies>`_ represent software that must be installed before the package builds or is able to work correctly.

Updating Dependencies
~~~~~~~~~~~~~~~~~~~~~

It is important that dependencies reflect the requirements of listed versions.
They only need to be checked in a review when versions are being added or removed or the dependencies are being changed.

**Action.**
Dependencies affected by such changes should be confirmed, when possible, and *at least* when the :ref:`Package Contributor <package-contributors>` is not a :ref:`Maintainer <package-maintainers>` of the package.

**Solutions.**
In some cases, the needed change may be as simple as ensuring the version range and or variant options in the dependency are accurate.
In others, one or more of the dependencies needed by new versions are missing and need to be added.
Or there may be dependencies that are no longer relevant when versions requiring them are removed, meaning the dependencies should be removed as well.

For example, it is not uncommon for Python package dependencies to be out of date when new versions are added.
In this case, check Python package dependencies by following the build system `guidelines <https://spack.readthedocs.io/en/latest/build_systems/pythonpackage.html#dependencies>`_.

.. tip::

    In general, refer to the relevant dependencies section, if any, for the package’s `build system <https://spack.readthedocs.io/en/latest/build_systems.html>`_ for guidance.

Updating Language and Compiler Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When `language and compiler dependencies <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#language-and-compiler-dependencies>`_ were introduced, their ``depends_on`` directives were derived from the source for existing packages.
These dependencies are flagged with ``# generated`` comments.
Unfortunately, the generated dependencies are not always complete.

**Action.**
If these dependencies are being updated, ask if the :ref:`Package Contributor <package-contributors>` can confirm all of the generated dependencies and remove the ``# generated`` comments.
Definitely make sure Contributors do **not** include ``# generated`` on the dependencies they are adding to the package.

Failed Automated Checks
-----------------------

All PRs are expected to pass **at least the required** automated checks.

Style Failures
~~~~~~~~~~~~~~

The PR may fail one or more style checks.

**Action.**
If the failure is due to issues raised by the ``black`` style checker *and* the PR is otherwise ready to be merged, you can add ``@spackbot fix style`` in a comment to see if Spack will fix the errors.
Otherwise, inform the Package Contributor that they need to address the style failures.

CI Stack Failures
~~~~~~~~~~~~~~~~~

Existing packages **may** be included in GitLab CI pipelines through inclusion in one or more `stacks <https://github.com/spack/spack-packages/tree/develop/stacks>`_.

**Action.**
It is worth checking at least a sampling of the failed job logs, if present, to determine the possible cause and take or suggest an action accordingly.

**CI runners.**
Sometimes CI runners time out or the pods become unavailable.

**Action.**
If that is the case, the resolution may be as simple as restarting the pipeline by adding a ``@spackbot run pipeline`` comment.
Otherwise, the Contributor will need to investigate and resolve the problem.

**Stand-alone tests.**
Sometimes `stand-alone tests <https://spack.readthedocs.io/en/latest/packaging_guide_testing.html#stand-alone-tests>`_, which are performed after successful builds, could be causing the build job to time out.
If the tests take too long, the issue could be that the package is running too many and/or long running tests.
Or the tests may be trying to use resources (e.g., a batch scheduler) that are not available on runners.
Determination of the problem may require looking at the implementation of the test.

**Action.**
If tests are to blame, then a `new issue <https://github.com/spack/spack-packages/issues>`_ should be created -- if there is not one already -- to flag the package.
A pull request should also be created in the ``spack/spack-packages`` repository that adds the package to the ``broken-tests-packages`` list in the `ci configuration <https://spack.readthedocs.io/en/latest/pipelines.html#ci-yaml>`_.
Then, after the hopefully temporary fix is merged, the PR being reviewed can be rebased to pick up the change.
