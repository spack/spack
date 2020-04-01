---
name: "\U0001F4A5 Build error" 
about: Some package in Spack didn't build correctly  
labels: "build-error"
---

<!--*Thanks for taking the time to report this build failure. To proceed with the
report please:*
1. Title the issue "Installation issue: <name-of-the-package>".
2. Provide the information required below.

We encourage you to try, as much as possible, to reduce your problem to the minimal example that still reproduces the issue. That would help us a lot in fixing it quickly and effectively!
-->


### Spack version
<!-- Add the output to the command below -->
```console
$ spack --version

```

### Steps to reproduce the issue

```console
$ spack install <spec> # Fill in the exact spec you are using
... # and the relevant part of the error message
```

### Platform and user environment

<!-- Please report your OS here:
```commandline
$ uname -a 
Linux nuvolari 4.15.0-29-generic #31-Ubuntu SMP Tue Jul 17 15:39:52 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
$ lsb_release -d
Description:	Ubuntu 18.04.1 LTS
``` 
and, if relevant, post or attach:

- `packages.yaml`
- `compilers.yaml`

to the issue
-->

### Additional information

<!--Sometimes the issue benefits from additional details. In these cases there are
a few things we can suggest doing. First of all, you can post the full output of:
```console
$ spack spec --install-status <spec>
...
```
to show people whether Spack installed a faulty software or if it was not able to
build it at all. 

If your build didn't make it past the configure stage, Spack as also commands to parse 
logs and report error and warning messages:
```console
$ spack log-parse --show=errors,warnings <file-to-parse>
```
You might want to run this command on the `config.log` or any other similar file
found in the stage directory: 
```console
$ spack location -s <spec>
```
In case in `config.log` there are other settings that you think might be the cause 
of the build failure, you can consider attaching the file to this issue.

Rebuilding the package with the following options:
```console
$ spack -d install -j 1 <spec>
...
```
will provide additional debug information. After the failure you will find two files in the current directory:

1. `spack-cc-<spec>.in`, which contains details on the command given in input 
    to Spack's compiler wrapper  
1. `spack-cc-<spec>.out`, which contains the command used to compile / link the 
    failed object after Spack's compiler wrapper did its processing 

You can post or attach those files to provide maintainers with more information on what
is causing the failure.-->

### General information

- [ ] I have run `spack --version` and reported the version of Spack
- [ ] I have searched the issues of this repo and believe this is not a duplicate
