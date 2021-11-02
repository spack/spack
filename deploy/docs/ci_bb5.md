# Using Spack for Continuous Integration on BlueBrain5

When building Spack packages with Jenkins, please use the `bb5` executors.
Then you will be able to install software with:

    $ module load unstable git
    $ git clone -c feature.manyFiles=true https://github.com/BlueBrain/spack.git
    $ . spack/share/spack/setup-env.sh
    $ mkdir fake_home
    $ export HOME=${PWD}/fake_home
    $ mkdir -p ~/.spack
    $ ln -s /gpfs/bbp.cscs.ch/apps/hpc/jenkins/config/*.yaml ~/.spack
    $ export SPACK_INSTALL_PREFIX=${HOME}/software
    $ spack build-dev <my_package>

*Note that a custom home directory is created* to avoid any interference from
a shared configuration of Spack.
