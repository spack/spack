# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Track different reggistered CI pipeline job classes."""
import spack.error

#: Registered CI job (data) classes
_ci_job_classes = {}


def ci_job_class(name):
    """Decorator to register the default pipeline CIJobData class or a subclass.

    The constructor should take the name of the type of job, optional release
    spec, optional remove boolean. Additional keyword (kwargs) are also allowed.

    Args:
        name: name of the job class
    """

    def _decorator(ci_job_class):
        _ci_job_classes[name] = ci_job_class
        return name

    return _decorator


def get_ci_job_class(name):
    """Retrieve the registered pipeline job class.

    Args:
        name: pipeline target name

    Returns: The named pipeline's job class

    Raises:
        UnknownCIJobClass: no job class available for the target
    """
    try:
        return _ci_job_classes[name]
    except KeyError:
        raise UnknownCIJobClass(name)


class UnknownCIJobClass(spack.error.SpackError):
    def __init__(self, name: str):
        super().__init__(f"No registered job class available for {name}")
