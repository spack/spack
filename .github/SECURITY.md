# Security Policy

## Supported Versions

We provide security updates for `develop` and for the last two stable (`X.Y`) release series of Spack. Security updates will be made available as patch (`X.Y.1`, `X.Y.2`, etc.) releases. For more on Spack's release structure, see [`README.md`](https://github.com/spack/spack#releases).

## Issues That Are Not Security Vulnerabilities

The following examples _do not_ constitute security vulnerabilities:

* **Vulnerabilities in Spack packages.** See https://github.com/spack/spack-packages/security instead.
* **Vulnerabilities in the underlying operating system.** Spack relies on a number of [system dependencies](https://spack.readthedocs.io/en/latest/installing_prerequisites.html) such as Python, git, and tar. Older versions of these dependencies may contain vulnerabilities, and users should not use Spack if they do not trust the operating system it is running on.
* **Intentionally disabling or bypassing security features.** For example, the use of `spack install --no-checksum` or manually tampering with the download URL or checksum is not considered secure and is a user-mistake instead of a security vulnerability.

When in doubt, open a vulnerability report and check with us.

## Issues That Are Security Vulnerabilities

The following examples _do_ constitute security vulnerabilities:

* **Insecure usage of our dependencies.** For example, the use of `eval`, `exec`, `pickle.loads`, or `subprocess.run(shell=True)` are standard features of Python. But without proper input validation, they can result in arbitrary code execution.
* **Vulnerabilities in CI.** For example, a vulnerability that allows exfiltration of private API keys would constitute a security vulnerability, not in Spack, but in our release pipeline.
* **Security features that do not work as expected.** For example, GPG signing keys, checksum validation, or other security features should work as expected.

This list is not exhaustive, and we encourage you to report when in doubt.

## Known Security Considerations

Spack installs software from source by executing the build system of a package. This build system can execute arbitrary code that may write to locations outside of the expected build stage or installation prefix. Please enable our experimental [build isolation and sandboxing](https://spack.readthedocs.io/en/latest/installing.html#build-isolation-and-sandboxing-linux) to prevent this kind of security issue.

Spack guarantees the security of our `builtin` package repository. However, third-party package repositories are not maintained by Spack maintainers. In particular, Spack executes all package files in order to generate dependency metadata, not just the packages you request. We are working on metadata caching and sandboxing to resolve this. Until then, ensure you only use third-party package repositories from organizations you trust.

## Reporting a Vulnerability

You can report a vulnerability using GitHub's private reporting feature:

1. Go to [github.com/spack/spack/security](https://github.com/spack/spack/security).
2. Click "Report a vulnerability" in the upper right corner of that page.
3. Fill out the form and submit your draft security advisory.

More details are available in [GitHub's docs](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).

## Timeline

We typically strive for the following timeline:

1. Reported vulnerabilities will be investigated and you can expect feedback within two days.
2. Accepted vulnerabilities will be fixed and a new release will be made within one week.
3. Vulnerabilities will be disclosed after a standard 90-day wait period to allow users time to upgrade.

If fixing the issue will take longer than this, we will discuss timeline options with you.
