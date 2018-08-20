---
name: Bug report 
about: Report a bug in the core of Spack (command not working as expected, etc.) 

---


*Explain, in a clear and concise way, the command you ran and the result you were trying to achieve.
Example: "I ran Spack find to list all the installed packages and..."*



### Steps to reproduce the issue

```console
$ spack <command1> <spec>
$ spack <command2> <spec>
...
```

### Error Message

If Spack reported an error, provide the error message. If it did not report an error
but the output appears incorrect, provide the incorrect output. If there was no error
message and no output but the result is incorrect, describe how it does not match
what you expect. To provide more information you might re-run the commands with 
the additional -sd flags:
```console
$ spack -sd <command1> <spec>
$ spack -sd <command2> <spec>
...
```
that activate the full debug output. 


### Information on your system

This includes:

 1. which platform you are using
 2. any relevant configuration detail (custom `packages.yaml` or `modules.yaml`, etc.)

-----

We encourage you to try, as much as possible, to reduce your problem to the minimal example that still reproduces the issue. That would help us a lot in fixing it quickly and effectively!

If you want to ask a question about the tool (how to use it, what it can currently do, etc.), try the `#general` channel on our Slack first. We have a welcoming community and chances are you'll get your reply faster and without opening an issue.

Other than that, thanks for taking the time to contribute to Spack!