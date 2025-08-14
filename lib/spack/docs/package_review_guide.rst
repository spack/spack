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

Explain to the :ref:`Contributor <package-contributors>` in a comment or your review if the package should be removed from the PR and why.

CORE Perl Modules
~~~~~~~~~~~~~~~~~

In general, modules that are part of the standard installation for all listed Perl versions should *not* be implemented or contributed as Spack packages.
Details on the exceptions and process for checking Perl modules can be found in the `Perl <https://spack.readthedocs.io/en/latest/build_systems/perlpackage.html#suitable_perl_modules>`_ build system documentation.

url, url_for_version, or URL Equivalent
---------------------------------------

Changes to URLs may invalidate existing versions, which should be checked when there is a URL-related modification.
All packages have a URL, though for some `build systems <https://spack.readthedocs.io/en/latest/build_systems.html>`_ it is derived automatically and not visible in the package.

Reasons for `invalid versions <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#versions-and-urls>`_ include:

* the new URL does not support Spack version extrapolation;
* the addition of or changes to ``url_for_version`` checks the ``spec``'s version instead of the ``version`` argument or does not cover the listed or older versions;
* extrapolation of the derived URL no longer matches that of older versions; and
* the older versions are no longer available.

Checking existing version directives with checksums can usually be done manually with the modified package using `spack checksum <https://spack.readthedocs.io/en/latest/command_index.html#spack-checksum>`_.

**Solutions.** Options for resolving the problem that can be suggested for investigation depends on the issues.

In simpler cases involving ``url`` or ``url_for_version``, invalid versions can sometimes be corrected by ensuring all versions are covered by ``url_for_version``.
Alternatively, especially for older versions, the version-specific URL can be added as an argument to the ``version`` directive.

Sometimes the derived URLs of versions on the hosting system can vary.
This commonly happens with Python packages.
For example, the case of one or more letters in the package name can change (e.g., `py-sphinx <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/py_sphinx/package.py>`_).
Also, dashes may be replaced with underscores (e.g., `py-scitkit-build <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/py_scikit_build/package.py>`_).
In some cases, both changes can occur for the same package.
As these examples illlustrate, it is sometimes possible to add a ``url_for_version`` method to override the default derived URL process to ensure the correct URL is returned.

If older versions are no longer available and there is a chance someone has the package in a build cache, the usual approach is to first suggest `deprecating <https://spack.readthedocs.io/en/latest/packaging_guide.html#deprecating-old-versions>`_ them in the package.

Maintainers Directive
----------------------

If the new package does not have a **maintainers** directive, ask the
:ref:`Package Contributor <package-contributors>` if he/she/they would be
willing to add themselves as a `maintainer <https://spack.readthedocs.io/en/latest/packaging_guide.html#maintainers>`_.

This request is an optional for existing packages.

.. tip::

   Be prepared for them to refuse.

License Directive
-----------------

If the new package does not have a **license** directive, ask the
`Package Contributor <#package-contributors>`__ if he/she/they would be
willing to check the source repository or homepage for the `license <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#license-information>`_ and add it to the package.

This is an optional request for existing packages.

Version Directives
------------------

Spack packages are, with a few exceptions (e.g., `BundlePackage <https://spack.readthedocs.io/en/latest/build_systems/bundlepackage.html#bundlepackage>`_), expected to be built from source code.
Typically every package will have at least one `version directive <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#source-code-and-versions>`_.

The goal of reviewing this information is to confirm the existence and correctness of updated and new versions **and** that the versions are listed in descending order from newest to oldest.
Additions and removals of version directives should also trigger a review of :ref:`dependencies <depends_on_reviews>`.

Checksums, commits, tags, and branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checksums, commits, and tags.**
Normally these arguments are automatically validated by GitHub Actions using `spack ci verify-versions <https://spack.readthedocs.io/en/latest/command_index.html#spack-ci-verify-versions>`_.
Review the ``verify-checksums`` precheck to confirm.
Checksums can usually be manually confirmed using `spack checksum <https://spack.readthedocs.io/en/latest/command_index.html#spack-checksum>`_.

.. warning::

   From a security and reproducibility standpoint, it is important that Spack be able to verify downloaded source.
   This is accomplished using a hash (e.g., checksum or commit).
   See `checksum verification <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#checksum-verification>`_ for more information.

   Exceptions are allowed in rare cases, such as software supplied from reputable vendors.
   When in doubt, ask others with merge privileges for advice.

If a ``tag`` is provided without a ``commit``, the downloaded software will not be trusted.
Suggest that the ``commit`` argument be included in the ``version`` directive.

**Branches.**
Confirming branches exist, on the other hand, often involves checking the source repository.

In general, the name of a branch version should match the name of the branch in the repository.
Sometimes they do not match when people are not aware of how Spack handles `version ordering <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#version-comparison>`_.
If there is a mismatch, especially for the most common branch names (e.g., `develop`, `main`, and `master`), ask why and suggest the arguments be changed such that they match the actual branch name.

**Manual downloads.**
Edge cases, such as manually downloaded software, may be difficult to confirm.
In these cases it is acceptable to rely on the package's maintainers, if any.

Deprecating Versions
~~~~~~~~~~~~~~~~~~~~

If someone is deprecating versions, it is good to know why.
Sometimes there are concerns with `versions <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#source-code-and-versions>`_ , especially older ones.
Suggest the Contributor review the `deprecation guidelines <https://spack.readthedocs.io/en/latest/packaging_guide.html#deprecating-old-versions>`_ before finalizing the changes if they haven't already explained why they made the choice in the PR description or comments.

Variant Directives
------------------

`Variants <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#variants>`_ represent build options so any changes involving these directives should be reflected elsewhere in the package.

Adding or Modifying Variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Confirm that new or modified variants are actually used in the package.
The most common uses are additions or changes to:

* dependencies;
* configure options; and/or
* build arguments.

Removing or Disabling Variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the variant is still relevant to listed version directives, it may be preferable to adjust or add `conditions <https://spack.readthedocs.io/en/latest/packaging_guide.html#conditional-variants>`_.
Consider asking why the variant (or build option) is being removed and mention the option to make it conditional.

.. warning::

    If the default value of a variant is changed, there is a risk that other packages relying on that value will no longer build as others expect.
    This may be something worth noting in the review.

.. _depends_on_reviews:

Depends_on Directives
---------------------

`Dependencies <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#dependencies>`_ represent software that must be installed before the package builds or is able to work correctly.

Updating Dependencies
~~~~~~~~~~~~~~~~~~~~~

It is important that dependencies reflect the requirements of listed versions.
So they only need to be checked in a review when versions are being added or removed or the dependencies are being changed.
In some cases, the needed change may be as simple as ensuring the version range and or variant options are accurate.
In others, one or more of the dependencies needed by new versions may be missing.
Or there may be dependencies that are no longer relevant as when the versions requiring them are removed.
Dependencies affected by version directive changes should be confirmed, when possible, and *at least* when the Contributor is not a Maintainer of the package.

For example, it is not uncommon for Python package dependencies to be out of date when new versions are added.
Check for missing dependencies by following the Python build system `guidelines <https://spack.readthedocs.io/en/latest/build_systems/pythonpackage.html#dependencies>`_.

.. tip::

    In general, refer to the relevant dependencies section, if any, for the package’s `build system <https://spack.readthedocs.io/en/latest/build_systems.html>`_ for guidance.

Updating Language and Compiler Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At one point `language and compiler dependencies <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#language-and-compiler-dependencies>`_
were derived for existing packages.
These dependencies are flagged with “# generated” comments.
Unfortunately, they are not always complete.

If these types of dependencies are being updated, suggest that if the Contributor is confirming them, then the `# generated` comments should be removed from all such dependencies.
Definitely make sure they do **not** include the comment on any they are adding to the package.

Failed Automated Checks
-----------------------

All PRs are expected to pass **at least the required** automated checks.

Style Failures
~~~~~~~~~~~~~~

The PR may fail one or more style checks.

If the failure is due to issues raised by the ``black`` style checker *and* the PR is otherwise ready to be merge, you can add a ``@spackbot fix style`` as a comment to see if Spack will fix the errors.
Otherwise, add a comment to the Contributor that they need to address the style failures.

CI Stack Failures
~~~~~~~~~~~~~~~~~

Existing packages **may** be included in GitLab CI pipelines through inclusion in one or more `stacks <https://github.com/spack/spack-packages/tree/develop/stacks>`_.
It is worth checking at least a sampling of the failed job logs, if present, to determine the possible cause.

**CI runners.**
Sometimes CI runners can timeout or the pods become unavailable.

If that is the case, the resolution may be as simple as restarting the pipeline by adding ``@spackbot run pipeline`` in a comment.

**Stand-alone tests.**
Or `stand-alone tests <https://spack.readthedocs.io/en/latest/packaging_guide_testing.html#stand-alone-tests>`_) performed after successful builds could be to blame.
If the tests take too long, the issue could be that the package is running too many or too resource intensive checks.
Or the tests may be trying to use resources (e.g., a batch scheduler) that are not available.
Determination of the problem may require looking at the implementation of the test.

If tests are to blame, then an `issue <https://github.com/spack/spack-packages/issues>`_ should be created to flag the package.
A `pull request <https://github.com/spack/spack-packages/pulls>`_ should also be created that adds the package to the **broken-tests-packages** list in the `ci <https://spack.readthedocs.io/en/latest/pipelines.html#ci-yaml>`_ configuration.
Then, after the hopefully temporary fix is merged, the PR being reviewed can be rebased to pick up the change.
