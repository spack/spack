.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      This is a guide for people who review package pull requests and includes criteria for them to be merged into the develop branch.

.. _package-review-guide:

Package Review Guide
====================

Package reviews are performed with the goals of minimizing build errors and making packages as **uniform and stable** as possible.

This section establishes guidelines to help assess Spack community `package repository <https://github.com/spack/spack-packages>`_ pull requests (PRs).
It describes the considerations and actions to be taken when reviewing new and updated `Spack packages <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#structure-of-a-package>`_.
In some cases, there are possible solutions to common issues.

How to use this guide
---------------------

Whether you are a :ref:`Package Reviewer <package-reviewers>`, :ref:`Maintainer <package-maintainers>`, or :ref:`Committer <committers>`, this guide highlights relevant aspects to consider when reviewing package pull requests.
If you are a :ref:`Package Contributor <package-contributors>` (or simply ``Contributor``), you may also find the information and solutions useful in your work.
While we provide information on what to look for, the changes themselves should drive the actual review process.

.. note::

   :ref:`Confirmation of successful package builds <build_success_reviews>` of **all** affected versions can reduce the amount of effort needed to review a PR.
   However, packaging conventions and the combinatorial nature of versions and directives mean each change should still be checked.

Reviewing a new package
~~~~~~~~~~~~~~~~~~~~~~~

If the pull request includes a new package, then focus on answering the following questions:

* Should the :ref:`package <suitable_package>` be added to the repository?
* Does the package :ref:`structure <structure_reviews>` conform to conventions?
* Are the directives and their options correct?
* Do all :ref:`automated checks <automated_checks_reviews>` pass?
  If not, are there easy-to-resolve CI and/or test issues that can be addressed or does the submitter need to investigate the failures?
* Is there :ref:`confirmation <build_success_reviews>` that every version builds successfully on at least one platform?

Refer to the relevant sections below for more guidance.

Reviewing changes to an existing package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the pull request includes changes to an existing package, then focus on answering the following questions:

* Are there any changes to the package :ref:`structure <structure_reviews>` and, if so, do they conform to conventions?
* If there are new or updated directives, then are they and their options correct?
* If there are changes to the :ref:`url or its equivalent <url_equivalent_reviews>`, are the older versions still correct?
* If there are changes to the :ref:`git or equivalent URL <vcs_url_reviews>`, do older branches exist in the new location?
* Do all :ref:`automated checks <automated_checks_reviews>` pass?
  If not, are there easy-to-resolve CI and/or test issues that can be addressed or does the submitter need to investigate the failures?
* Is there :ref:`confirmation <build_success_reviews>` that every new version builds successfully on at least one platform?

Refer to the relevant sections below for more guidance.

.. _suitable_package:

Package suitability
-------------------

It is rare that a package would be considered inappropriate for inclusion in the public `Spack package <https://github.com/spack/spack-packages>`_ repository.
One exception is making packages for standard Perl modules.

**Action.**
Should you find the software is not appropriate, ask that the package be removed from the PR if it is one of multiple affected files or suggest the PR be closed.
In either case, explain the reason for the request.

CORE Perl modules
~~~~~~~~~~~~~~~~~

In general, modules that are part of the standard installation for all listed Perl versions (i.e., ``CORE``) should **not be implemented or contributed**.
Details on the exceptions and process for checking Perl modules can be found in the :ref:`Perl build system <suitable_perl_modules>` documentation.

.. _structure_reviews:

Package structure
-----------------

The `convention <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#structure-of-a-package>`_ for structuring Spack packages has metadata (key properties) listed first followed by directives then methods:

* :ref:`url_equivalent_reviews`;
* :ref:`vcs_url_reviews`;
* :ref:`maintainers_reviews`;
* :ref:`license_reviews`;
* :ref:`version_reviews`;
* :ref:`variant_reviews`;
* :ref:`depends_on_reviews`;
* :ref:`packaging_conflicts` and :ref:`packaging_requires` directives; then
* methods.

`Groupings <https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#grouping-directives>`_ using ``with`` context managers can affect the order of dependency, conflict, and requires directives to some degree.
However, they do cut down on visual clutter and make packages more readable.

**Action.**
If you see clear deviations from the convention, request that they be addressed.
When in doubt, ask others with merge privileges for advice.

.. _url_equivalent_reviews:

``url``, ``url_for_version``, or URL equivalent
-----------------------------------------------

Changes to URLs may invalidate existing versions, which should be checked when there is a URL-related modification.
All packages have a URL, though for some :ref:`build-systems` it is derived automatically and not visible in the package.

Reasons :ref:`versions <versions-and-fetching>` may become invalid include:

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
Also, dashes may be replaced with underscores (e.g., `py-scikit-build <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/py_scikit_build/package.py>`_).
In some cases, both changes can occur for the same package.
As these examples illlustrate, it is sometimes possible to add a ``url_for_version`` method to override the default derived URL to ensure the correct one is returned.

If older versions are no longer available and there is a chance someone has the package in a build cache, the usual approach is to first suggest :ref:`deprecating <deprecate>` them in the package.

.. _vcs_url_reviews:

``git``, ``hg``, ``svn``, or ``cvs``
------------------------------------

If the :ref:`repository-specific URL <vcs-fetch>` for fetching branches or the version control system (VCS) equivalent changes, there is a risk that the listed versions are no longer accessible.

**Action.**
You may need to check the new source repository to confirm the presence of all of the listed versions.

.. _maintainers_reviews:

``maintainers`` directive
-------------------------

**Action.**
If the new package does not have a :ref:`maintainers <maintainers>` directive, ask the Contributor to add one.

.. note::

   This request is optional for existing packages.

   Be prepared for them to refuse.

.. _license_reviews:

``license`` directive
---------------------

**Action.**
If the new package does not have a :ref:`license <package_license>` directive, ask the Contributor to investigate and add it.

.. note::

   This request is optional for existing packages.

   Be prepared for them to refuse.

.. _version_reviews:

``version`` directives
----------------------

In general, Spack packages are expected to be built from source code.
There are a few exceptions (e.g., :ref:`BundlePackage <bundlepackage>`).
Typically every package will have at least one :ref:`version <versions-and-fetching>` directive.

The goals of reviewing version directives are to confirm that versions are listed in the proper order **and** that the arguments for new and updated versions are correct.

.. note::

   Additions and removals of version directives should generally trigger a review of :ref:`dependencies <depends_on_reviews>`.

``version`` directive order
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By :ref:`convention <versions-and-fetching>` version directives should be listed in descending order, from newest to oldest.
If branch versions are included, then they should be listed first.

**Action.**
When versions are being added, check the ordering of the directives.
Request that the directives be  re-ordered if any of the directives do not conform to the convention.

.. note::

   Edge cases, such as manually downloaded software, may be difficult to confirm.

Checksums, commits, tags, and branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checksums, commits, and tags**
  Normally these version arguments are automatically validated by GitHub Actions using `spack ci verify-versions <https://spack.readthedocs.io/en/latest/command_index.html#spack-ci-verify-versions>`_.

  **Action.**
  Review the PR's ``verify-checksums`` precheck to confirm.
  If necessary, checksums can usually be manually confirmed using `spack checksum <https://spack.readthedocs.io/en/latest/command_index.html#spack-checksum>`_.

  .. warning::

     From a security and reproducibility standpoint, it is important that Spack be able to verify downloaded source.
     This is accomplished using a hash (e.g., checksum or commit).
     See :ref:`checksum verification <checksum-verification>` for more information.

     Exceptions are allowed in rare cases, such as software supplied from reputable vendors.
     When in doubt, ask others with merge privileges for advice.

**Tags**
  If a ``tag`` is provided without a ``commit``, the downloaded software will not be trusted.

  **Action.**
  Suggest that the ``commit`` argument be included in the ``version`` directive.

**Branches**
  Confirming new branch versions involves checking that the branches exist in the repository *and* that the version and branch names are consistent.
  Let's take each in turn.

  **Action.**
  Confirming branch existence often involves checking the source repository though is not necessary if there is confirmation that the branch was built successfully from the package.

  In general, the version and branch names should match.
  When they do not, it is sometimes the result of people not being aware of how Spack handles :ref:`version-comparison`.

  **Action.**
  If there is a name mismatch, especially for the most common branch names (e.g., ``develop``, ``main``, and ``master``), ask why and suggest the arguments be changed such that they match the actual branch name.

**Manual downloads**

  **Action.**
  Since these can be difficult to confirm, it is acceptable to rely on the package's Maintainers, if any.

Deprecating versions
~~~~~~~~~~~~~~~~~~~~

If someone is deprecating versions, it is good to find out why.
Sometimes there are concerns, such as security or lack of availability.

**Action.**
Suggest the Contributor review the :ref:`deprecation guidelines <deprecate>` before finalizing the changes if they haven't already explained why they made the choice in the PR description or comments.

.. _variant_reviews:

``variant`` directives
----------------------

:ref:`Variants <variants>` represent build options so any changes involving these directives should be reflected elsewhere in the package.

Adding or modifying variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Action.**
Confirm that new or modified variants are actually used in the package.
The most common uses are additions and changes to:

* :ref:`dependencies <depends_on_reviews>`;
* configure options; and/or
* build arguments.

Removing or disabling variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the variant is still relevant to listed version directives, it may be preferable to adjust or add `conditions <https://spack.readthedocs.io/en/latest/packaging_guide.html#conditional-variants>`_.

**Action.**
Consider asking why the variant (or build option) is being removed and suggest making it conditional when it is still relevant.

.. warning::

    If the default value of a variant is changed in the PR, then there is a risk that other packages relying on that value will no longer build as others expect.
    This may be worth noting in the review.

.. _depends_on_reviews:

``depends_on`` directives
-------------------------

:ref:`Dependencies <dependencies>` represent software that must be installed before the package builds or is able to work correctly.

Updating dependencies
~~~~~~~~~~~~~~~~~~~~~

It is important that dependencies reflect the requirements of listed versions.
They only need to be checked in a review when versions are being added or removed or the dependencies are being changed.

**Action.**
Dependencies affected by such changes should be confirmed, when possible, and *at least* when the Contributor is not a Maintainer of the package.

**Solutions.**
In some cases, the needed change may be as simple as ensuring the version range and or variant options in the dependency are accurate.
In others, one or more of the dependencies needed by new versions are missing and need to be added.
Or there may be dependencies that are no longer relevant when versions requiring them are removed, meaning the dependencies should be removed as well.

For example, it is not uncommon for Python package dependencies to be out of date when new versions are added.
In this case, check Python package dependencies by following the build system `guidelines <https://spack.readthedocs.io/en/latest/build_systems/pythonpackage.html#dependencies>`_.

.. tip::

    In general, refer to the relevant dependencies section, if any, for the package’s :ref:`build-systems` for guidance.

Updating language and compiler dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When :ref:`language and compiler dependencies <language-dependencies>` were introduced, their ``depends_on`` directives were derived from the source for existing packages.
These dependencies are flagged with ``# generated`` comments when they have not been confirmed.
Unfortunately, the generated dependencies are not always complete or necessarily required.

**Action.**
If these dependencies are being updated, ask that the ``# generated`` comments be removed if the Contributor can confirm they are relevant.
Definitely make sure Contributors do **not** include ``# generated`` on the dependencies they are adding to the package.

.. _automated_checks_reviews:

Failed automated checks
-----------------------

All PRs are expected to pass **at least the required** automated checks.

Style failures
~~~~~~~~~~~~~~

The PR may fail one or more style checks.

**Action.**
If the failure is due to issues raised by the ``black`` style checker *and* the PR is otherwise ready to be merged, you can add ``@spackbot fix style`` in a comment to see if Spack will fix the errors.
Otherwise, inform the Contributor that the style failures need to be addressed.

CI stack failures
~~~~~~~~~~~~~~~~~

Existing packages **may** be included in GitLab CI pipelines through inclusion in one or more `stacks <https://github.com/spack/spack-packages/tree/develop/stacks>`_.

**Action.**
It is worth checking **at least a sampling** of the failed job logs, if present, to determine the possible cause and take or suggest an action accordingly.

**CI Runner Failures**
  Sometimes CI runners time out or the pods become unavailable.

  **Action.**
  If that is the case, the resolution may be as simple as restarting the pipeline by adding a ``@spackbot run pipeline`` comment.
  Otherwise, the Contributor will need to investigate and resolve the problem.

**Stand-alone Test Failures**
  Sometimes :ref:`stand-alone tests <cmd-spack-test>` could be causing the build job to time out.
  If the tests take too long, the issue could be that the package is running too many and/or long running tests.
  Or the tests may be trying to use resources (e.g., a batch scheduler) that are not available on runners.

  **Action.**
  If the tests for a package are hanging, at a minimum create a `new issue <https://github.com/spack/spack-packages/issues>`_ if there is not one already, to flag the package.

  **(Temporary) Solution.**
  Look at the package implementation to see if the tests are using a batch scheduler or there appear to be too many or long running tests.
  If that is the case, then a pull request should be created in the ``spack/spack-packages`` repository that adds the package to the ``broken-tests-packages`` list in the `ci configuration <https://spack.readthedocs.io/en/latest/pipelines.html#ci-yaml>`_.
  Once the fix PR is merged, then the affected PR can be rebased to pick up the change.

.. _build_success_reviews:

Successful builds
-----------------

Is there evidence that the package builds successfully on at least one platform?
For a new package, we would ideally have confirmation for every version; whereas, we would want confirmation of only the affected versions for changes to an existing package.

Acceptable forms of confirmation are **one or more of**:

* the Contributor or another reviewer explicitly confirms that a successful build of **each new version on at least one platform**;
* the software is built successfully by Spack CI by **at least one of the CI stacks**; and
* **at least one Maintainer** explicitly confirms they are able to successfully build the software.

Individuals are expected to update the PR description or add a comment to explicitly confirm the builds.
You may need to check the CI stacks and/or outputs to confirm that there is a stack that builds the new version.

.. note::

   When builds are confirmed by individuals, we would prefer the output of ``spack debug report`` be included in either the PR description or a comment.
