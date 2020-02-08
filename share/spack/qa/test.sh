# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

export QA_DIR=$(dirname "$0")
export SHARE_DIR=$(cd "$QA_DIR/.." && pwd)
export SPACK_ROOT=$(cd "$QA_DIR/../../.." && pwd)

. "$QA_DIR/test-framework.sh"

fail
pass
