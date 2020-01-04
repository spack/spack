# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import re
import sys


def load_spack_micros(spack_micro_file):
    micros = json.load(spack_micro_file)['microarchitectures']
    non_generic = (k for k in micros if micros[k]['vendor'] != 'generic')
    return set(non_generic)


def load_openblas_micros(target_file):
    re_target = re.compile(r'^[A-Z0-9_]+$')

    micros = []
    for line in target_file:
        match = re_target.match(line)
        if match is not None:
            micros.append(line.strip().lower())
    return set(micros)


def main():
    # Path to $SPACK_ROOT/lib/spack/llnl/util/cpu/microarchitectures.json
    # and path to ${OPENBLAS_SOURCE}/TargetList.txt
    (micro_json, openblas_targets) = sys.argv[1:]

    with open(micro_json, 'r') as f:
        spack_micros = load_spack_micros(f)

    with open(openblas_targets, 'r') as f:
        openblas_micros = load_openblas_micros(f)

    print("Spack - OpenBLAS:\n ",
          "\n  ".join(sorted(spack_micros - openblas_micros)))
    print("OpenBLAS - Spack:\n ",
          "\n  ".join(sorted(openblas_micros - spack_micros)))


if __name__ == "__main__":
    main()
