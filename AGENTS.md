This is a tool called "Spack"

- Spack is for installing packages and managing dependencies
- It is a command line tool and all the commands are subcommands of "spack", like "spack install..."

General information:

- Documentation for spack is in lib/spack/docs/
- Unit tests for spack are in lib/spack/spack/tests/
- Spack has a notion of package repositories, there are several test ones, for example in var/spack/test_repos/spack_repo/builtin_mock/
- The "real" spack packages repository is generally stored outside of spack, but can be found with `spack repo list` (look for "builtin")