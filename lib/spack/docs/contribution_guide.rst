.. _contribution-guide:

==================
Contribution Guide
==================

This guide is intended for developers or administrators who want to
contribute a new package, feature, or bugfix to Spack.
It assumes that you have at least some familiarity with Git VCS and Github.
The guide will show a few examples of contributing workflows and discuss
the granularity of pull-requests (PRs). It will also discuss the tests your
PR must pass in order to be accepted into Spack.

First, what is a PR? Quoting `Bitbucket's tutorials <https://www.atlassian.com/git/tutorials/making-a-pull-request/>`_:

  Pull requests are a mechanism for a developer to notify team members that
  they have **completed a feature**. The pull request is more than just a
  notification—it’s a dedicated forum for discussing the proposed feature.

Important is **completed feature**. The changes one proposes in a PR should
correspond to one feature/bugfix/extension/etc. One can create PRs with
changes relevant to different ideas, however reviewing such PRs becomes tedious
and error prone. If possible, try to follow the **one-PR-one-package/feature** rule.

Spack uses a rough approximation of the `Git Flow <http://nvie.com/posts/a-successful-git-branching-model/>`_
branching model. The develop branch contains the latest contributions, and
master is always tagged and points to the latest stable release. Therefore, when
you send your request, make ``develop`` the destination branch on the
`Spack repository <https://github.com/LLNL/spack>`_.

----------------------
Continuous Integration
----------------------

Spack uses `Travis CI <https://travis-ci.org/LLNL/spack>`_ for Continuous Integration
testing. This means that every time you submit a pull request, a series of tests will
be run to make sure you didn't accidentally introduce any bugs into Spack. Your PR
will not be accepted until it passes all of these tests. While you can certainly wait
for the results of these tests after submitting a PR, we recommend that you run them
locally to speed up the review process.

If you take a look in ``$SPACK_ROOT/.travis.yml``, you'll notice that we test
against Python 2.6 and 2.7. We currently perform 3 types of tests:

^^^^^^^^^^
Unit Tests
^^^^^^^^^^

Unit tests ensure that core Spack features like fetching or spec resolution are
working as expected. If your PR only adds new packages or modifies existing ones,
there's very little chance that your changes could cause the unit tests to fail.
However, if you make changes to Spack's core libraries, you should run the unit
tests to make sure you didn't break anything.

Since they test things like fetching from VCS repos, the unit tests require
`git <https://git-scm.com/>`_, `mercurial <https://www.mercurial-scm.org/>`_,
and `subversion <https://subversion.apache.org/>`_ to run. Make sure these are
installed on your system and can be found in your ``PATH``. All of these can be
installed with Spack or with your system package manager.

To run *all* of the unit tests, use:

.. code-block:: console

   $ spack test

These tests may take several minutes to complete. If you know you are only
modifying a single Spack feature, you can run a single unit test at a time:

.. code-block:: console

   $ spack test architecture

This allows you to develop iteratively: make a change, test that change, make
another change, test that change, etc. To get a list of all available unit
tests, run:

.. command-output:: spack test --list

A more detailed list of available unit tests can be found by running
``spack test --long-list``.

Unit tests are crucial to making sure bugs aren't introduced into Spack. If you
are modifying core Spack libraries or adding new functionality, please consider
adding new unit tests or strengthening existing tests.

.. note::

   There is also a ``run-unit-tests`` script in ``share/spack/qa`` that
   runs the unit tests. Afterwards, it reports back to Coverage with the
   percentage of Spack that is covered by unit tests. This script is
   designed for Travis CI. If you want to run the unit tests yourself, we
   suggest you use ``spack test``.

^^^^^^^^^^^^
Flake8 Tests
^^^^^^^^^^^^

Spack uses `Flake8 <http://flake8.pycqa.org/en/latest/>`_ to test for
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ conformance. PEP 8 is
a series of style guides for Python that provide suggestions for everything
from variable naming to indentation. In order to limit the number of PRs that
were mostly style changes, we decided to enforce PEP 8 conformance. Your PR
needs to comply with PEP 8 in order to be accepted.

Testing for PEP 8 compliance is easy. Simply run the ``spack flake8``
command:

.. code-block:: console

   $ spack flake8

``spack flake8`` has a couple advantages over running ``flake8`` by hand:

#. It only tests files that you have modified since branching off of
   ``develop``.

#. It works regardless of what directory you are in.

#. It automatically adds approved exemptions from the ``flake8``
   checks. For example, URLs are often longer than 80 characters, so we
   exempt them from line length checks. We also exempt lines that start
   with "homepage", "url", "version", "variant", "depends_on", and
   "extends" in ``package.py`` files.

More approved flake8 exemptions can be found
`here <https://github.com/LLNL/spack/blob/develop/.flake8>`_.

If all is well, you'll see something like this:

.. code-block:: console

   $ run-flake8-tests
   Dependencies found.
   =======================================================
   flake8: running flake8 code checks on spack.

   Modified files:

     var/spack/repos/builtin/packages/hdf5/package.py
     var/spack/repos/builtin/packages/hdf/package.py
     var/spack/repos/builtin/packages/netcdf/package.py
   =======================================================
   Flake8 checks were clean.

However, if you aren't compliant with PEP 8, flake8 will complain:

.. code-block:: console

   var/spack/repos/builtin/packages/netcdf/package.py:26: [F401] 'os' imported but unused
   var/spack/repos/builtin/packages/netcdf/package.py:61: [E303] too many blank lines (2)
   var/spack/repos/builtin/packages/netcdf/package.py:106: [E501] line too long (92 > 79 characters)
   Flake8 found errors.

Most of the error messages are straightforward, but if you don't understand what
they mean, just ask questions about them when you submit your PR. The line numbers
will change if you add or delete lines, so simply run ``run-flake8-tests`` again
to update them.

.. tip::

   Try fixing flake8 errors in reverse order. This eliminates the need for
   multiple runs of ``flake8`` just to re-compute line numbers and makes it
   much easier to fix errors directly off of the Travis output.

.. warning::

   Flake8 requires setuptools in order to run. If you installed ``py-flake8``
   with Spack, make sure to add ``py-setuptools`` to your ``PYTHONPATH``.
   Otherwise, you will get an error message like:

   .. code-block:: console

      Traceback (most recent call last):
        File: "/usr/bin/flake8", line 5, in <module>
          from pkg_resources import load_entry_point
      ImportError: No module named pkg_resources

^^^^^^^^^^^^^^^^^^^
Documentation Tests
^^^^^^^^^^^^^^^^^^^

Spack uses `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ to build its
documentation. In order to prevent things like broken links and missing imports,
we added documentation tests that build the documentation and fail if there
are any warning or error messages.

Building the documentation requires several dependencies, all of which can be
installed with Spack:

* sphinx
* graphviz
* git
* mercurial
* subversion

.. warning::

   Sphinx has `several required dependencies <https://github.com/LLNL/spack/blob/develop/var/spack/repos/builtin/packages/py-sphinx/package.py>`_.
   If you installed ``py-sphinx`` with Spack, make sure to add all of these
   dependencies to your ``PYTHONPATH``. The easiest way to do this is to run
   ``spack activate py-sphinx`` so that all of the dependencies are symlinked
   to a central location. If you see an error message like:

   .. code-block:: console

      Traceback (most recent call last):
        File: "/usr/bin/flake8", line 5, in <module>
          from pkg_resources import load_entry_point
      ImportError: No module named pkg_resources

   that means Sphinx couldn't find setuptools in your ``PYTHONPATH``.

Once all of the dependencies are installed, you can try building the documentation:

.. code-block:: console

   $ cd "$SPACK_ROOT/lib/spack/docs"
   $ make clean
   $ make

If you see any warning or error messages, you will have to correct those before
your PR is accepted.

.. note::

   There is also a ``run-doc-tests`` script in the Quality Assurance directory.
   The only difference between running this script and running ``make`` by hand
   is that the script will exit immediately if it encounters an error or warning.
   This is necessary for Travis CI. If you made a lot of documentation tests, it
   is much quicker to run ``make`` by hand so that you can see all of the warnings
   at once.

If you are editing the documentation, you should obviously be running the
documentation tests. But even if you are simply adding a new package, your
changes could cause the documentation tests to fail:

.. code-block:: console

   package_list.rst:8745: WARNING: Block quote ends without a blank line; unexpected unindent.

At first, this error message will mean nothing to you, since you didn't edit
that file. Until you look at line 8745 of the file in question:

.. code-block:: rst

   Description:
      NetCDF is a set of software libraries and self-describing, machine-
     independent data formats that support the creation, access, and sharing
     of array-oriented scientific data.

Our documentation includes :ref:`a list of all Spack packages <package-list>`.
If you add a new package, its docstring is added to this page. The problem in
this case was that the docstring looked like:

.. code-block:: python

   class Netcdf(Package):
       """
       NetCDF is a set of software libraries and self-describing,
       machine-independent data formats that support the creation,
       access, and sharing of array-oriented scientific data.
       """

Docstrings cannot start with a newline character, or else Sphinx will complain.
Instead, they should look like:

.. code-block:: python

   class Netcdf(Package):
       """NetCDF is a set of software libraries and self-describing,
       machine-independent data formats that support the creation,
       access, and sharing of array-oriented scientific data."""

Documentation changes can result in much more obfuscated warning messages.
If you don't understand what they mean, feel free to ask when you submit
your PR.

-------------
Git Workflows
-------------

Spack is still in the beta stages of development. Most of our users run off of
the develop branch, and fixes and new features are constantly being merged. So
how do you keep up-to-date with upstream while maintaining your own local
differences and contributing PRs to Spack?

^^^^^^^^^
Branching
^^^^^^^^^

The easiest way to contribute a pull request is to make all of your changes on
new branches. Make sure your ``develop`` is up-to-date and create a new branch
off of it:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git branch <descriptive_branch_name>
   $ git checkout <descriptive_branch_name>

Here we assume that the local ``develop`` branch tracks the upstream develop
branch of Spack. This is not a requirement and you could also do the same with
remote branches. But for some it is more convenient to have a local branch that
tracks upstream.

Normally we prefer that commits pertaining to a package ``<package-name>`` have
a message ``<package-name>: descriptive message``. It is important to add
descriptive message so that others, who might be looking at your changes later
(in a year or maybe two), would understand the rationale behind them.

Now, you can make your changes while keeping the ``develop`` branch pure.
Edit a few files and commit them by running:

.. code-block:: console

   $ git add <files_to_be_part_of_the_commit>
   $ git commit --message <descriptive_message_of_this_particular_commit>

Next, push it to your remote fork and create a PR:

.. code-block:: console

   $ git push origin <descriptive_branch_name> --set-upstream

GitHub provides a `tutorial <https://help.github.com/articles/about-pull-requests/>`_
on how to file a pull request. When you send the request, make ``develop`` the
destination branch.

If you need this change immediately and don't have time to wait for your PR to
be merged, you can always work on this branch. But if you have multiple PRs,
another option is to maintain a Frankenstein branch that combines all of your
other branches:

.. code-block:: console

   $ git co develop
   $ git branch <your_modified_develop_branch>
   $ git checkout <your_modified_develop_branch>
   $ git merge <descriptive_branch_name>

This can be done with each new PR you submit. Just make sure to keep this local
branch up-to-date with upstream ``develop`` too.

^^^^^^^^^^^^^^
Cherry-Picking
^^^^^^^^^^^^^^

What if you made some changes to your local modified develop branch and already
committed them, but later decided to contribute them to Spack? You can use
cherry-picking to create a new branch with only these commits.

First, check out your local modified develop branch:

.. code-block:: console

   $ git checkout <your_modified_develop_branch>

Now, get the hashes of the commits you want from the output of:

.. code-block:: console

   $ git log

Next, create a new branch off of upstream ``develop`` and copy the commits
that you want in your PR:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git branch <descriptive_branch_name>
   $ git checkout <descriptive_branch_name>
   $ git cherry-pick <hash>
   $ git push origin <descriptive_branch_name> --set-upstream

Now you can create a PR from the web-interface of GitHub. The net result is as
follows:

#. You patched your local version of Spack and can use it further.
#. You "cherry-picked" these changes in a stand-alone branch and submitted it
   as a PR upstream.

Should you have several commits to contribute, you could follow the same
procedure by getting hashes of all of them and cherry-picking to the PR branch.

.. note::

   It is important that whenever you change something that might be of
   importance upstream, create a pull request as soon as possible. Do not wait
   for weeks/months to do this, because:

   #. you might forget why you modified certain files
   #. it could get difficult to isolate this change into a stand-alone clean PR.

^^^^^^^^
Rebasing
^^^^^^^^

Other developers are constantly making contributions to Spack, possibly on the
same files that your PR changed. If their PR is merged before yours, it can
create a merge conflict. This means that your PR can no longer be automatically
merged without a chance of breaking your changes. In this case, you will be
asked to rebase on top of the latest upstream ``develop``.

First, make sure your develop branch is up-to-date:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop

Now, we need to switch to the branch you submitted for your PR and rebase it
on top of develop:

.. code-block:: console

   $ git checkout <descriptive_branch_name>
   $ git rebase develop

Git will likely ask you to resolve conflicts. Edit the file that it says can't
be merged automatically and resolve the conflict. Then, run:

.. code-block:: console

   $ git add <file_that_could_not_be_merged>
   $ git rebase --continue

You may have to repeat this process multiple times until all conflicts are resolved.
Once this is done, simply force push your rebased branch to your remote fork:

.. code-block:: console

   $ git push --force origin <descriptive_branch_name>

^^^^^^^^^^^^^^^^^^^^^^^^^
Rebasing with cherry-pick
^^^^^^^^^^^^^^^^^^^^^^^^^

You can also perform a rebase using ``cherry-pick``. First, create a temporary
backup branch:

.. code-block:: console

   $ git checkout <descriptive_branch_name>
   $ git branch tmp

If anything goes wrong, you can always go back to your ``tmp`` branch.
Now, look at the logs and save the hashes of any commits you would like to keep:

.. code-block:: console

   $ git log

Next, go back to the original branch and reset it to ``develop``.
Before doing so, make sure that you local ``develop`` branch is up-to-date
with upstream:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git checkout <descriptive_branch_name>
   $ git reset --hard develop

Now you can cherry-pick relevant commits:

.. code-block:: console

   $ git cherry-pick <hash1>
   $ git cherry-pick <hash2>

Push the modified branch to your fork:

.. code-block:: console

   $ git push --force origin <descriptive_branch_name>

If everything looks good, delete the backup branch:

.. code-block:: console

   $ git branch --delete --force tmp

^^^^^^^^^^^^^^^^^^
Re-writing History
^^^^^^^^^^^^^^^^^^

Sometimes you may end up on a branch that has diverged so much from develop
that it cannot easily be rebased. If the current commits history is more of
an experimental nature and only the net result is important, you may rewrite
the history.

First, merge upstream ``develop`` and reset you branch to it. On the branch
in question, run:

.. code-block:: console

   $ git merge develop
   $ git reset develop

At this point your branch will point to the same commit as develop and
thereby the two are indistinguishable. However, all the files that were
previously modified will stay as such. In other words, you do not lose the
changes you made. Changes can be reviewed by looking at diffs:

.. code-block:: console

   $ git status
   $ git diff

The next step is to rewrite the history by adding files and creating commits:

.. code-block:: console

   $ git add <files_to_be_part_of_commit>
   $ git commit --message <descriptive_message>

After all changed files are committed, you can push the branch to your fork
and create a PR:

.. code-block:: console

   $ git push origin --set-upstream
