# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc

get_job_name = lambda needs_entry: (
    needs_entry.get("job")
    if (isinstance(needs_entry, collections.abc.Mapping) and needs_entry.get("artifacts", True))
    else needs_entry
    if isinstance(needs_entry, str)
    else None
)


def convert_job(job_entry):
    if not isinstance(job_entry, collections.abc.Mapping):
        return job_entry

    needs = job_entry.get("needs")
    if needs is None:
        return job_entry

    new_job = {}
    new_job.update(job_entry)
    del new_job["needs"]

    new_job["dependencies"] = list(
        filter((lambda x: x is not None), (get_job_name(needs_entry) for needs_entry in needs))
    )

    return new_job


def needs_to_dependencies(yaml):
    return dict((k, convert_job(v)) for k, v in yaml.items())
