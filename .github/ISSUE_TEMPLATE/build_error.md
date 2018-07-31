---
name: Build error 
about: Some package in Spack didn't build correctly  

---

*Thanks for taking the time to report this build failure. To proceed with the
report please:*
1. Title the issue "Installation issue: <name-of-the-package>".
1. Provide the information required below.
1. Clean the issue from these template instructions.

### Steps to reproduce the issue

```console
$ spack install <spec> # Fill in the exact spec you are using
... # and the relevant part of the error message
```

### Platform and user environment

Please report here your OS:
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

### Additional information

If you think this report would benefit from additional details, e.g. extracts 
from the logs in `<stage>/spack-build.out`, or the output of some other:
```console
$ spack <command>
```   
please insert those things here. 

-----

We encourage you to try, as much as possible, to reduce your problem to the minimal example that still reproduces the issue. That would help us a lot in fixing it quickly and effectively!

If you want to ask a question about the tool (how to use it, what it can currently do, etc.), try the `#general` channel on our Slack first. We have a welcoming community and chances are you'll get your reply faster and without opening an issue.

Other than that, thanks for taking the time to contribute to Spack!