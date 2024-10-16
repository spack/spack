# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#!/bin/sh

if [ "$CI_JOB_STATUS" != "failed" ]; then
    exit 0
fi

if ["$CI_RUNNER_TAGS" != *"aws"*]; then
    exit 0
fi

proc1_cgroup=$(cat /proc/1/cgroup)

(
  dmesg | grep -q "oom-kill.*$(echo "$proc1_cgroup" | tr / '\n' | tail -1)" \
    && echo "oom kill"
) || (
  dmesg | grep -q "oom-kill.*$(echo "$proc1_cgroup" | tr / '\n' | tail -2 | head -1)" \
    && echo "oom kill pod"
) || true


