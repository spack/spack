#!/bin/bash
    (echo "spack:" \
&&   echo "  specs: []" \
&&   echo "  container:" \
&&   echo "    format: docker" \
&&   echo "    images:" \
&&   echo "      os: \"${SPACK_YAML_OS}\"" \
&&   echo "      spack:" \
&&   echo "        resolve_sha: True" \
&&   echo "        ref: ${GITHUB_REF}") > spack.yaml
