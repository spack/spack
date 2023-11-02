Upstreaming packages
====================

Getting your packages to upstream
---------------------------------

The easiest way to do this is to create your own fork of [Spack](https://github.com/spack/spack). Create a new branch starting from the latest `develop` branch and copy your changes there. Your package recipe and any patches should go under `var/spack/repos/builtin/packages/`.

You'll need to:
  * make sure a recent (preferably the latest) version is present in the recipe
  * if specifying a version linked to a git branch, ensure the version name and branch name are the same
  * make sure dependencies are correct and complete
    * give them the correct type. For Python dependencies `type=("build", "run")` in most cases
    * for Python packages: no need to specify `py-wheel` or `py-pip`, those come with the parent class
    * when adding multiple versions, keep in mind that different versions can have different dependencies, versions of dependencies, ...
  * ensure your code is properly formatted (black) and the header is correct (including the copyright year)
  * an upstreamed package should not depend on anything internal - it should install from your spack fork without any bluebrain-specific modifications

Create your pull request from your fork to the Spack `develop` branch and go through the review process.

Backporting upstreamed changes
------------------------------

Once your pull request has been merged, you'll need to backport your changes to our own spack repository. In order to do this, there's a script available: `bluebrain/bin/upstream.sh`.
If you call it without arguments, it will explain how to use it.

Prepare to run by creating the branch you'd like to commit your changes to.

---
**WARNING**: if you have a local branch called `upstream-develop` it **will** be reset to match upstream/develop
---

The first argument is the name of the package you've upstreamed
The optional second argument can be 'update' to update your `upstream-develop` branch from `upstream/develop`. Typically you'll update upstream only on the first package in your batch.

The script will:
  * if necessary, create the upstream remote pointing to github.com:spack/spack
  * if asked (through the 'update' argument), checkout upstream-develop tracking upstream/develop, `git pull` and go back to the branch you were on when you started
  * `git checkout` the upstream/develop version of your upstreamed package (the first argument) in var/spack/repos/builtin/packages
  * for whatever exists of your package under `bluebrain/repo-{patches,bluebrain}/packages/`: `git rm` and `rm -rf`
  
Now you can commit, push and file a pull request to [our own Spack repository](https://github.com/bluebrain/spack).
