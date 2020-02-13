.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _pipelines:

=========
Pipelines
=========

Spack provides commands that support generating and running automated build
pipelines designed for Gitlab CI.  At the highest level it works like this:
provide a spack environment describing the set of packages you care about,
and include within that environment file a description of how those packages
should be mapped to Gitlab runners.  Spack can then generate a ``.gitlab-ci.yml``
file containing job descriptions for all your packages that can be run by a
properly configured Gitlab CI instance.  When run, the generated pipeline will
build and deploy binaries, and it can optionally report to a CDash instance
regarding the health of the builds as they evolve over time.

------------------------------
Getting started with pipelines
------------------------------

It is fairly straightforward to get started with automated build pipelines.  At
a minimum, you'll need to set up a Gitlab instance (more about Gitlab CI
`here <https://about.gitlab.com/product/continuous-integration/>`_) and configure
at least one `runner <https://docs.gitlab.com/runner/>`_.  Then the basic steps
for setting up a build pipeline are as follows:

#. Create a repository on your gitlab instance
#. Add a ``spack.yaml`` at the root containing your pipeline environment (see
   below for details)
#. Add a ``.gitlab-ci.yml`` at the root containing a single job, similar to
   this one:

   .. code-block:: yaml

      pipeline-job:
        tags:
          - <custom-tag>
          ...
        script:
          - spack ci start

#. Add any secrets required by the CI process to environment variables using the
   CI web ui
#. Push a commit containing the ``spack.yaml`` and ``.gitlab-ci.yml`` mentioned above
   to the gitlab repository

The ``<custom-tag>``, above, is used to pick one of your configured runners,
while the use of the ``spack ci start`` command implies that runner has an
appropriate version of spack installed and configured for use.  Of course, there
are myriad ways to customize the process.  You can configure CDash reporting
on the progress of your builds, set up S3 buckets to mirror binaries built by
the pipeline, clone a custom spack repository/ref for use by the pipeline, and
more.

While it is possible to set up pipelines on gitlab.com, the builds there are
limited to 60 minutes and generic hardware.  It is also possible to
`hook up <https://about.gitlab.com/blog/2018/04/24/getting-started-gitlab-ci-gcp>`_
Gitlab to Google Kubernetes Engine (`GKE <https://cloud.google.com/kubernetes-engine/>`_)
or Amazon Elastic Kubernetes Service (`EKS <https://aws.amazon.com/eks>`_), though those
topics are outside the scope of this document.

-----------------------------------
Spack commands supporting pipelines
-----------------------------------

Spack provides a command `ci` with sub-commands for doing various things related
to automated build pipelines.  All of the ``spack ci ...`` commands must be run
from within a environment, as each one makes use of the environment for different
purposes.  Additionally, some options to the commands (or conditions present in
the spack environment file) may require particular environment variables to be
set in order to function properly.  Examples of these are typically secrets
needed for pipeline operation that should not be visible in a spack environment
file.  These environment variables are described in more detail
:ref:`ci_environment_variables`.

.. _cmd_spack_ci:

^^^^^^^^^^^^^^^^^^
``spack ci``
^^^^^^^^^^^^^^^^^^

Super-command for functionality related to generating pipelines and executing
pipeline jobs.

.. _cmd_spack_ci_start:

^^^^^^^^^^^^^^^^^^
``spack ci start``
^^^^^^^^^^^^^^^^^^

Currently this command is a short-cut to first run ``spack ci generate``, followed
by ``spack ci pushyaml``.

.. _cmd_spack_ci_generate:

^^^^^^^^^^^^^^^^^^^^^
``spack ci generate``
^^^^^^^^^^^^^^^^^^^^^

Concretizes the specs in the active environment, stages them (as described in
:ref:`staging_algorithm`), and writes the resulting ``.gitlab-ci.yml`` to disk.

.. _cmd_spack_ci_pushyaml:

^^^^^^^^^^^^^^^^^^^^^
``spack ci pushyaml``
^^^^^^^^^^^^^^^^^^^^^

Generates a commit containing the generated ``.gitlab-ci.yml`` and pushes it to a
``DOWNSTREAM_CI_REPO``, which is frequently the same repository.  The branch
created has the same name as the current branch being tested, but has ``multi-ci-``
prepended to the branch name.  Once Gitlab CI has full support for dynamically
defined workloads, this command will be deprecated.

.. _cmd_spack_ci_rebuild:

^^^^^^^^^^^^^^^^^^^^
``spack ci rebuild``
^^^^^^^^^^^^^^^^^^^^

This sub-command is responsible for ensuring a single spec from the release
environment is up to date on the remote mirror configured in the environment,
and as such, corresponds to a single job in the ``.gitlab-ci.yml`` file.

------------------------------------
A pipeline-enabled spack environment
------------------------------------

Here's an example of a spack environment file that has been enhanced with
sections desribing a build pipeline:

.. code-block:: yaml

   spack:
     definitions:
     - pkgs:
       - readline@7.0
     - compilers:
       - '%gcc@5.5.0'
     - oses:
       - os=ubuntu18.04
       - os=centos7
     specs:
     - matrix:
       - [$pkgs]
       - [$compilers]
       - [$oses]
     mirrors:
       cloud_gitlab: https://mirror.spack.io
     gitlab-ci:
       mappings:
         - match:
             - os=ubuntu18.04
           runner-attributes:
             tags:
               - spack-k8s
             image: spack/spack_builder_ubuntu_18.04
         - match:
             - os=centos7
           runner-attributes:
             tags:
               - spack-k8s
             image: spack/spack_builder_centos_7
     cdash:
       build-group: Release Testing
       url: https://cdash.spack.io
       project: Spack
       site: Spack AWS Gitlab Instance

Hopefully, the ``definitions``, ``specs``, ``mirrors``, etc. sections are already
familiar, as they are part of spack :ref:`environments`.  So let's take a more
in-depth look some of the pipeline-related sections in that environment file
that might not be as familiar.

The ``gitlab-ci`` section is used to configure how the pipeline workload should be
generated, mainly how the jobs for building specs should be assigned to the
configured runners on your instance.  Each entry within the list of ``mappings``
corresponds to a known gitlab runner, where the ``match`` section is used
in assigning a release spec to one of the runners, and the ``runner-attributes``
section is used to configure the spec/job for that particular runner.

There are other pipeline options you can configure within the ``gitlab-ci`` section
as well.  The ``bootstrap`` section allows you to specify lists of specs from
your ``definitions`` that should be staged ahead of the environment's ``specs`` (this
section is described in more detail below).  The ``enable-artifacts-buildcache`` key
takes a boolean and determines whether the pipeline uses artifacts to store and
pass along the buildcaches from one stage to the next (the default if you don't
provide this option is ``False``).  The ``enable-debug-messages`` key takes a boolean
and allows you to choose whether the pipeline build jobs are run as ``spack -d ci rebuild``
or just ``spack ci rebuild`` (the default is not to enable debug messages).  The
``final-stage-rebuild-index`` section controls whether an extra job is added to the
end of your pipeline (in a stage by itself) which will regenerate the mirror's
buildcache index.  Under normal operation, each pipeline job that rebuilds a package
will re-generate the mirror's buildcache index after the buildcache entry for that
job has been created and pushed to the mirror.  Since jobs in the same stage can run in
parallel, there is the possibility that at the end of some stage, the index may not
reflect all the binaries in the buildcache.  Adding the ``final-stage-rebuild-index``
section ensures that at the end of the pipeline, the index will be in sync with the
binaries on the mirror.  If the mirror lives in an S3 bucket, this job will need to
run on a machine with the Python ``boto3`` module installed, and consequently the
``final-stage-rebuild-index`` needs to specify a list of ``tags`` to pick a runner
satisfying that condition.  It can also take an ``image`` key so Docker executor type
runners can pick the right image for the index regeneration job.

The optional ``cdash`` section provides information that will be used by the
``spack ci generate`` command (invoked by ``spack ci start``) for reporting
to CDash.  All the jobs generated from this environment will belong to a
"build group" within CDash that can be tracked over time.  As the release
progresses, this build group may have jobs added or removed. The url, project,
and site are used to specify the CDash instance to which build results should
be reported.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Assignment of specs to runners
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``mappings`` section corresponds to a list of runners, and during assignment
of specs to runners, the list is traversed in order looking for matches, the
first runner that matches a release spec is assigned to build that spec.  The
``match`` section within each runner mapping section is a list of specs, and
if any of those specs match the release spec (the ``spec.satisfies()`` method
is used), then that runner is considered a match.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configuration of specs/jobs for a runner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once a runner has been chosen to build a release spec, the ``runner-attributes``
section provides information determining details of the job in the context of
the runner.  The ``runner-attributes`` section must have a ``tags`` key, which
is a list containing at least one tag used to select the runner from among the
runners known to the gitlab instance.  For Docker executor type runners, the
``image`` key is used to specify the Docker image used to build the release spec
(and could also appear as a dictionary with a ``name`` specifying the image name,
as well as an ``entrypoint`` to override whatever the default for that image is).
For other types of runners the ``variables`` key will be useful to pass any
information on to the runner that it needs to do its work (e.g. scheduler
parameters, etc.).

.. _staging_algorithm:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Summary of ``.gitlab-ci.yml`` generation algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All specs yielded by the matrix (or all the specs in the environment) have their
dependencies computed, and the entire resulting set of specs are staged together
before being run through the ``gitlab-ci/mappings`` entries, where each staged
spec is assigned a runner.  "Staging" is the name we have given to the process
of figuring out in what order the specs should be built, taking into consideration
Gitlab CI rules about jobs/stages.  In the staging process the goal is to maximize
the number of jobs in any stage of the pipeline, while ensuring that the jobs in
any stage only depend on jobs in previous stages (since those jobs are guaranteed
to have completed already).  As a runner is determined for a job, the information
in the ``runner-attributes`` is used to populate various parts of the job
description that will be used by Gitlab CI. Once all the jobs have been assigned
a runner, the ``.gitlab-ci.yml`` is written to disk.

The short example provided above would result in the ``readline``, ``ncurses``,
and ``pkgconf`` packages getting staged and built on the runner chosen by the
``spack-k8s`` tag.  In this example, we assume the runner is a Docker executor
type runner, and thus certain jobs will be run in the ``centos7`` container,
and others in the ``ubuntu-18.04`` container.  The resulting ``.gitlab-ci.yml``
will contain 6 jobs in three stages.  Once the jobs have been generated, the
presence of a ``SPACK_CDASH_AUTH_TOKEN`` environment variable during the
``spack ci generate`` command would result in all of the jobs being put in a
build group on CDash called "Release Testing" (that group will be created if
it didn't already exist).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optional compiler bootstrapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack pipelines also have support for bootstrapping compilers on systems that
may not already have the desired compilers installed. The idea here is that
you can specify a list of things to bootstrap in your ``definitions``, and
spack will guarantee those will be installed in a phase of the pipeline before
your release specs, so that you can rely on those packages being available in
the binary mirror when you need them later on in the pipeline.  At the moment
the only viable use-case for bootstrapping is to install compilers.

Here's an example of what bootstrapping some compilers might look like:

.. code-block:: yaml

   spack:
     definitions:
     - compiler-pkgs:
       - 'llvm+clang@6.0.1 os=centos7'
       - 'gcc@6.5.0 os=centos7'
       - 'llvm+clang@6.0.1 os=ubuntu18.04'
       - 'gcc@6.5.0 os=ubuntu18.04'
     - pkgs:
       - readline@7.0
     - compilers:
       - '%gcc@5.5.0'
       - '%gcc@6.5.0'
       - '%gcc@7.3.0'
       - '%clang@6.0.0'
       - '%clang@6.0.1'
     - oses:
       - os=ubuntu18.04
       - os=centos7
     specs:
     - matrix:
       - [$pkgs]
       - [$compilers]
       - [$oses]
       exclude:
         - '%gcc@7.3.0 os=centos7'
         - '%gcc@5.5.0 os=ubuntu18.04'
     gitlab-ci:
       bootstrap:
         - name: compiler-pkgs
           compiler-agnostic: true
       mappings:
         # mappings similar to the example higher up in this description
         ...

In the example above, we have added a list to the ``definitions`` called
``compiler-pkgs`` (you can add any number of these), which lists compiler packages
we want to be staged ahead of the full matrix of release specs (which consists
only of readline in our example).  Then within the ``gitlab-ci`` section, we
have added a ``bootstrap`` section, which can contain a list of items, each
referring to a list in the ``definitions`` section.  These items can either
be a dictionary or a string.  If you supply a dictionary, it must have a name
key whose value must match one of the lists in definitions and it can have a
``compiler-agnostic`` key whose value is a boolean.  If you supply a string,
then it needs to match one of the lists provided in ``definitions``.  You can
think of the bootstrap list as an ordered list of pipeline "phases" that will
be staged before your actual release specs.  While this introduces another
layer of bottleneck in the pipeline (all jobs in all stages of one phase must
complete before any jobs in the next phase can begin), it also means you are
guaranteed your bootstrapped compilers will be available when you need them.

The ``compiler-agnostic`` key can be provided with each item in the
bootstrap list. It tells the ``spack ci generate`` command that any jobs staged
from that particular list should have the compiler removed from the spec, so
that any compiler available on the runner where the job is run can be used to
build the package.

When including a bootstrapping phase as in the example above, the result is that
the bootstrapped compiler packages will be pushed to the binary mirror (and the
local artifacts mirror) before the actual release specs are built. In this case,
the jobs corresponding to subsequent release specs are configured to
``install_missing_compilers``, so that if spack is asked to install a package
with a compiler it doesn't know about, it can be quickly installed from the
binary mirror first.

Since bootstrapping compilers is optional, those items can be left out of the
environment/stack file, and in that case no bootstrapping will be done (only the
specs will be staged for building) and the runners will be expected to already
have all needed compilers installed and configured for spack to use.

-------------------------------------
Using a custom spack in your pipeline
-------------------------------------

If your runners will not have a version of spack ready to invoke, or if for some
other reason you want to use a custom version of spack to run your pipelines,
this can be accomplished fairly simply.  First, create CI environment variables
containing the url and branch/tag you want to clone (calling them, for example,
``SPACK_REPO`` and ``SPACK_REF``), use them to clone spack in your pre-ci
``before_script``, and finally pass those same values along to the workload
generation process via the ``spack-repo`` and ``spack-ref`` cli args.  Here's
an example:

.. code-block:: yaml

   pipeline-job:
     tags:
       - <some-other-tag>
   before_script:
     - git clone ${SPACK_REPO} --branch ${SPACK_REF}
     - . ./spack/share/spack/setup-env.sh
   script:
     - spack ci start --spack-repo ${SPACK_REPO} --spack-ref ${SPACK_REF} <...args>
   after_script:
     - rm -rf ./spack

If the ``spack ci start`` command receives those extra command line arguments,
then it adds similar ``before_script`` and ``after_script`` sections for each of
the ``spack ci rebuild`` jobs it generates (cloning and sourcing a custom
spack in the ``before_script`` and removing it again in the ``after_script``).
This gives you control over the version of spack used when the rebuild jobs
are actually run on the gitlab runner.

.. _ci_environment_variables:

--------------------------------------------------
Environment variables affecting pipeline operation
--------------------------------------------------

Certain secrets and some other information should be provided to the pipeline
infrastructure via environment variables, usually for reasons of security, but
in some cases to support other pipeline use cases such as PR testing.  The
environment variables used by the pipeline infrastructure are described here.

^^^^^^^^^^^^^^^^^
AWS_ACCESS_KEY_ID
^^^^^^^^^^^^^^^^^

Needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^^^^^^^
AWS_SECRET_ACCESS_KEY
^^^^^^^^^^^^^^^^^^^^^

Needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^
S3_ENDPOINT_URL
^^^^^^^^^^^^^^^

Needed when binary mirror is an S3 bucket that is *not* on AWS.

^^^^^^^^^^^^^^^^^
CDASH_AUTH_TOKEN
^^^^^^^^^^^^^^^^^

Needed in order to report build groups to CDash.

^^^^^^^^^^^^^^^^^
SPACK_SIGNING_KEY
^^^^^^^^^^^^^^^^^

Needed to sign/verify binary packages from the remote binary mirror.

^^^^^^^^^^^^^^^^^^
DOWNSTREAM_CI_REPO
^^^^^^^^^^^^^^^^^^

Needed until Gitlab CI supports dynamic job generation.  Can contain connection
credentials, and could be the same repository or a different one.
