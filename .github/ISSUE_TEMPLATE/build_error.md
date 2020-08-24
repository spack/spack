---
name: "\U0001F4A5 Build error"
about: Some package in Spack didn't build correctly
title: "Installation issue: "
labels: "build-error"
---

<!-- Thanks for taking the time to report this build failure. To proceed with the report please:

1. Title the issue "Installation issue: <name-of-the-package>".
2. Provide the information required below.

We encourage you to try, as much as possible, to reduce your problem to the minimal example that still reproduces the issue. That would help us a lot in fixing it quickly and effectively! -->

### Steps to reproduce the issue

<!-- Fill in the exact spec you are trying to build and the relevant part of the error message -->
```console
$ spack install <spec>
...
```

### Information on your system

<!-- Please include the output of `spack debug report` -->

<!-- If you have any relevant configuration detail (custom `packages.yaml` or `modules.yaml`, etc.) you can add that here as well. -->

### Additional information

<!-- Please upload the following files. They should be present in the stage directory of the failing build. Also upload any config.log or similar file if one exists. -->
* [spack-build-out.txt]()
* [spack-build-env.txt]()

<!-- Some packages have maintainers who have volunteered to debug build failures. Run `spack maintainers <name-of-the-package>` and @mention them here if they exist. -->

### General information

<!-- These boxes can be checked by replacing [ ] with [x] or by clicking them after submitting the issue. -->
- [ ] I have run `spack debug report` and reported the version of Spack/Python/Platform
- [ ] I have run `spack maintainers <name-of-the-package>` and @mentioned any maintainers
- [ ] I have uploaded the build log and environment files
- [ ] I have searched the issues of this repo and believe this is not a duplicate
