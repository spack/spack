---
name: "\U0001F41E Bug report"
about: Report a bug in the core of Spack (command not working as expected, etc.)
labels: "bug,triage"
---

<!-- Explain, in a clear and concise way, the command you ran and the result you were trying to achieve.
Example: "I ran `spack find` to list all the installed packages and ..." -->

### Steps to reproduce the issue

```console
$ spack <command1> <spec>
$ spack <command2> <spec>
...
```

### Error Message

<!-- If Spack reported an error, provide the error message. If it did not report an error but the output appears incorrect, provide the incorrect output. If there was no error message and no output but the result is incorrect, describe how it does not match what you expect. -->
```console
$ spack --debug --stacktrace <command>
```

### Information on your system

<!-- Please include the output of `spack debug report` -->

<!-- If you have any relevant configuration detail (custom `packages.yaml` or `modules.yaml`, etc.) you can add that here as well. -->

### Additional information

<!-- These boxes can be checked by replacing [ ] with [x] or by clicking them after submitting the issue. -->
- [ ] I have run `spack debug report` and reported the version of Spack/Python/Platform
- [ ] I have searched the issues of this repo and believe this is not a duplicate
- [ ] I have run the failing commands in debug mode and reported the output

<!-- We encourage you to try, as much as possible, to reduce your problem to the minimal example that still reproduces the issue. That would help us a lot in fixing it quickly and effectively!

If you want to ask a question about the tool (how to use it, what it can currently do, etc.), try the `#general` channel on our Slack first. We have a welcoming community and chances are you'll get your reply faster and without opening an issue.

Other than that, thanks for taking the time to contribute to Spack! -->
