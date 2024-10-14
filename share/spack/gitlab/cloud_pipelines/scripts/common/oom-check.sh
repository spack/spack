# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#!/bin/sh

if [ "$CI_JOB_STATUS" != "failed" ]; then
    exit 0
fi

# TODO if it's a UO runner then we don't want to check for OOM
echo $CI_RUNNER_DESCRIPTION
echo $CI_RUNNER_ID
echo $CI_RUNNER_SHORT_TOKEN
echo $CI_RUNNER_TAGS

proc1_cgroup=$(cat /proc/1/cgroup)

(
  dmesg | grep -q "oom-kill.*$(echo "$proc1_cgroup" | tr / '\n' | tail -1)" \
    && echo "oom kill"
) || (
  dmesg | grep -q "oom-kill.*$(echo "$proc1_cgroup" | tr / '\n' | tail -2 | head -1)" \
    && echo "oom kill pod"
) || true
