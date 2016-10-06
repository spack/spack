.. _contribution-guide:

Contribution Guide
=====================

This guide is intended for developers or administrators who want to
contribute a new package, feature, or bugfix to Spack.
It assumes that you have at least some familiarity with Git VCS and Github.
The guide will show a few examples of contributing workflow and discuss
the granularity of pull-requests (PRs).

First, what is a PR? Quoting `Bitbucket's tutorials <https://www.atlassian.com/git/tutorials/making-a-pull-request/>`_:

  Pull requests are a mechanism for a developer to notify team members that they have **completed a feature**.
  The pull request is more than just a notification—it’s a dedicated forum for discussing the proposed feature

Important is completed feature, i.e. the changes one propose in a PR should
correspond to one feature/bugfix/extension/etc. One can create PRs with
changes relevant to different ideas, however reviewing such PRs becomes tedious
and error prone. If possible, try to follow the rule **one-PR-one-package/feature.**

Spack uses a rough approximation of the `Git Flow <http://nvie.com/posts/a-successful-git-branching-model/>`_ branching
model. The develop branch contains the latest contributions, and master is
always tagged and points to the latest stable release. Thereby when you send
your request, make ``develop`` the destination branch on the
`Spack repository <https://github.com/LLNL/spack>`_.

Let's assume that the current (patched) state of your fork of Spack is only
relevant to yourself. Now you come across a bug in a package or would like to
extend a package and contribute this fix to Spack. It is important that
whenever you change something that might be of importance upstream,
create a pull-request (PR) as soon as possible. Do not wait for weeks/months to
do this: a) you might forget why did you modified certain files; b) it could get
difficult to isolate this change into a stand-alone clean PR.

Now let us discuss several approaches one may use to submit a PR while
also keeping your local version of Spack patched.


First approach (cherry-picking):
--------------------------------

First approach is as follows.
You checkout your local develop branch, which for the purpose of this guide
will be called ``develop_modified``:

.. code-block:: console

  $ git checkout develop_modified

Let us assume that lines in files you will be modifying
are the same in `develop_modified` branch and upstream ``develop``.
Next edit files, make sure they work for you and create a commit

.. code-block:: console

  $ git add <files_to_be_commited>
  $ git commit -m <descriptive note about changes>

Normally we prefer that commits pertaining to a package ``<package-name>``` have
a message ``<package-name>: descriptive message``. It is important to add
descriptive message so that others, who might be looking at your changes later
(in a year or maybe two), would understand the rationale behind.


Next we will create a branch off upstream's ``develop`` and copy this commit.
Before doing this, while still on your modified branch, get the hash of the
last commit

.. code-block:: console

  $ git log -1

and copy-paste this ``<hash>`` to the buffer. Now switch to upstream's ``develop``,
make sure it's updated, checkout the new branch, apply the patch and push to
GitHub:

.. code-block:: console

  $ git checkout develop
  $ git pull upstream develop
  $ git checkout -b <descriptive_branch_name>
  $ git cherry-pick <hash>
  $ git push <your_origin> <descriptive_branch_name> -u

Here we assume that local ``develop`` branch tracks upstream develop branch of
Spack. This is not a requirement and you could also do the same with remote
branches. Yet to some it is more convenient to have a local branch that
tracks upstream.

Now you can create a PR from web-interface of GitHub. The net result is as
follows:

#. You patched your local version of Spack and can use it further
#. You "cherry-picked" these changes in a stand-alone branch and submitted it
   as a PR upstream.


Should you have several commits to contribute, you could follow the same
procedure by getting hashes of all of them and cherry-picking to the PR branch.
This could get tedious and therefore there is another way:


Second approach:
----------------

In the second approach we start from upstream ``develop`` (again assuming
that your local branch `develop` tracks upstream):

.. code-block:: console

  $ git checkout develop
  $ git pull upstream develop
  $ git checkout -b <descriptive_branch_name>

Next edit a few files and create a few commits by

.. code-block:: console

  $ git add <files_to_be_part_of_the_commit>
  $ git commit -m <descriptive_message_of_this_particular_commit>

Now you can push it to your fork and create a PR

.. code-block:: console

  $ git push <your_origin> <descriptive_branch_name> -u

Most likely you would want to have those changes in your (modified) local
version of Spack. To that end you need to merge this branch

.. code-block:: console

  $ git checkout develop_modified
  $ git merge <descriptive_branch_name>

The net result is similar to the first approach with a minor difference that
you would also merge upstream develop into you modified version in the last
step. Should this not be desirable, you have to follow the first approach.



How to clean-up a branch by rewriting history:
-----------------------------------------------

Sometimes you may end up on a branch that has a lot of commits, merges of
upstream branch and alike but it can't be rebased on ``develop`` due to a long
and convoluted history. If the current commits history is more of an experimental
nature and only the net result is important, you may rewrite the history.
To that end you need to first merge upstream `develop` and reset you branch to
it. So on the branch in question do:

.. code-block:: console

   $ git merge develop
   $ git reset develop

At this point you your branch will point to the same commit as develop and
thereby the two are indistinguishable. However, all the files that were
previously modified will stay as such. In other words, you do not loose the
changes you made. Changes can be reviewed by looking at diffs

.. code-block:: console

   $ git status
   $ git diff

One can also run GUI to visualize the current changes

.. code-block:: console

   $ git difftool

Next step is to rewrite the history by adding files and creating commits

.. code-block:: console

   $ git add <files_to_be_part_of_commit>
   $ git commit -m <descriptive_message>


Shall you need to split changes within a file into separate commits, use

.. code-block:: console

   $ git add <file> -p

After all changed files are committed, you can push the branch to your fork
and create a PR

.. code-block:: console

   $ git push <you_origin> -u



How to fix a bad rebase by "cherry-picking" commits:
----------------------------------------------------

Say you are working on a branch ``feature1``. It has several commits and is
ready to be merged. However, there are a few minor merge conflicts and so
you are asked to rebase onto ``develop`` upstream branch. Occasionally, it
happens so that a contributor rebases not on top of the upstream branch, but
on his/her local outdated copy of it. This would lead to an inclusion of the
whole lot of duplicated history and of course can not be merged as-is.

One way to get out of troubles is to ``cherry-pick`` important commits. To
do that, first checkout a temporary back-up branch:

.. code-block:: console

  git checkout -b tmp

Now look at logs and save hashes of commits you would like to keep

.. code-block:: console

  git log

Next, go back to the original branch and reset it to ``develop``.
Before doing so, make sure that you local ``develop`` branch is up-to-date
with the upstream.

.. code-block:: console

  git checkout feature1
  git reset --hard develop

Now you can cherry-pick relevant commits

.. code-block:: console

  git cherry-pick  <hash1>
  git cherry-pick  <hash2>


push the modified branch to your fork

.. code-block:: console

  git push -f

and if everything looks good, delete the back-up:

.. code-block:: console

  git branch -D tmp
