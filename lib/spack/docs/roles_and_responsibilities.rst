.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A guide to distinguish the roles and responsibilities associated with managing the Spack Packages repository.

.. _packaging-roles:

Packaging Roles and Responsibilities
====================================

There are four roles related to `Spack Package <https://github.com/spack/spack-packages>`_ repository Pull Requests (PRs):

#. :ref:`package-contributors`,
#. :ref:`package-reviewers`,
#. :ref:`package-maintainers`, and
#. :ref:`committers`.

One person can assume multiple roles (e.g., a Package Contributor may also be a Maintainer; a Package Reviewer may also be a Committer).
This section defines and describes the responsibilities of each role.

.. _package-contributors:

Package Contributors
--------------------

Contributors submit changes to packages through PRs `Spack Package <https://github.com/spack/spack-packages>`_ repository Pull Requests (PRs).

As a Contributor, you are **expected** to test your changes on **at least one platform** outside of Spack’s Continuous Integration (CI) checks.

.. note::

   We also ask that you include the output from ``spack debug report`` from the platform you used to facilitate PR reviews.

.. _package-reviewers:

Package Reviewers
-----------------

Anyone can review a PR so we encourage Spack’s community members to review and comment on those involving software in which they have expertise and/or interest.

As a Package Reviewer, you are **expected** to assess changes in PRs to the best of your ability and knowledge with special consideration to the information contained in the :ref:`package-review-guide`.

.. _package-maintainers:

Maintainers (Package Owners)
----------------------------

Maintainers are individuals (technically GitHub accounts) who appear in a package’s :ref:`maintainers` directive.
These are people who have agreed to be notified of and given the opportunity to review changes to packages.
They are, from a Spack package perspective, `Code Owners <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>`_ of the package, whether or not they “own” or work on the software that the package builds.

As a Maintainer, you are **expected**, when available, to:

* review PRs in a timely manner (reported in :ref:`committers`) to confirm that the changes made to the package are reasonable;
* confirm that packages successfully build on at least one platform; and
* attempt to confirm that any updated or included tests pass.

See :ref:`build_success_reviews` for acceptable forms of build success confirmation.

.. note::

   If at least one maintainer approves a PR -– and there are no objections from others -– then the PR can be merged by any of the :ref:`committers`.

.. _committers:

Committers
----------

Committers are vetted individuals who are allowed to merge PRs into the ``develop`` branch.

As a Committer, you are **expected** to:

* ensure **at least one review** is performed prior to merging (GitHub rules enforce this);
* encourage **at least one** :ref:`Package Maintainer <package-maintainers>` (if any) to comment and/or review the PR;
* allow Package Maintainers (if any) **up to one week** to comment or provide a review;
* determine if the criteria defined in :ref:`package-review-guide` are met; and
* **merge the reviewed PR** at their discretion.

.. note::

   If there are no :ref:`package-maintainers` or the Maintainers have not commented or reviewed the PR within the allotted time, you will need to conduct the review.

.. tip::

   The following criteria must be met in order to become a Committer:

   * cannot be an anonymous account;
   * must come from a known and trustworthy organization;
   * demonstrated record of contribution to Spack;
   * have an account on the Spack Slack workspace;
   * be approved by the Onboarding subcommittee; and
   * (proposed) be known to at least 3 members of the core development team.
