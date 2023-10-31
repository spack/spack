# CI Build Reproduction

If one of your spack build jobs fails, spack provides an intriguing message:

```bash
To reproduce this build locally, run:
    spack ci reproduce-build https://bbpgitlab.epfl.ch/api/v4/projects/2136/jobs/984774/artifacts [--working-dir <dir>]
If this project does not have public pipelines, you will need to first:
    export GITLAB_PRIVATE_TOKEN=<generated_token>
... then follow the printed instructions.
```

Following these instructions (and then some) will allow you to reproduce the failure on your own machine.

Here's the more detailed version:

Start with a clean spack clone (`develop` branch unless you have a reason to take another branch)

> 💡 **NOTE**: if you’re working on the apple M1 runner (or any other node that might need it), make sure to set the proxy variables!
>
> ```bash
> export http_proxy=http://bbpproxy.epfl.ch:80
> export https_proxy=http://bbpproxy.epfl.ch:80
> export HTTP_PROXY=http://bbpproxy.epfl.ch:80
> export HTTPS_PROXY=http://bbpproxy.epfl.ch:80
> ```


> 💡 **NOTE**: there are two instances in this procedure where you’ll be asked to provide a gitlab access token.
> You can generate those on https://bbpgitlab.epfl.ch/-/profile/personal_access_tokens
>
> If you want to create only one token for this whole procedure, give it `read_api` and `read_repository` access.
> You can also split this into two tokens, one with each set of permissions.
> In that case, please make sure to use the correct token at the right time.


Within your spack clone directory:

```bash
source ./share/spack/setup-env.sh
# the spack command will be provided by your failed job - don't copy it from here!
spack ci reproduce-build https://bbpgitlab.epfl.ch/api/v4/projects/2136/jobs/984774/artifacts

# It will most likely complain that you need to run in the container that was used for the job
# on mac, don't forget to start your podman machine if necessary (you may need to do this on the M1 runner too)
podman machine start

# you'll need a gitlab token with at least read_repository access
podman login -u <your_gitlab_user> -p <your_gitlab_token> bbpgitlab.epfl.ch:5050

# make sure to edit the path and use the right container!
podman run --rm -v /path/to/your/spack/ci_reproduction:/builds/hpc/spack-cacher -ti --entrypoint=/bin/bash bbpgitlab.epfl.ch:5050/hpc/spacktainerizer/ubuntu_22.04/builder:2023.10.13-graviton
```

In the container:

```bash
# Only in the graviton version of the container
source /opt/spack/share/spack/setup-env.sh

# you'll need a gitlab token with at least read_api access
export GITLAB_PRIVATE_TOKEN=...

# these four steps are only needed if you're working with graviton!
# ##############################
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
rm /root/.spack/mirrors.yaml
spack mirror add bbpS3 s3://spack-cache-xlme2pbun4
# ##############################
# continue here if not working with graviton

# this command can be found in your failed job output - don't copy it here!
spack ci reproduce-build https://bbpgitlab.epfl.ch/api/v4/projects/2136/jobs/984774/artifacts

# it will complain and tell you the next commands to run.- don't copy them from here!
spack env activate --without-view /path/to/concrete_environment
/path/to/reproduction/install.sh
```
