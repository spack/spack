#!/bin/bash
#
# This script checks that Spack packages are installed in ~/.local.

NPKGS="$(./spack find -p | grep zlib | grep -Fo "$HOME/.local" | wc -l)"
if ! [[ "$NPKGS" == 1 ]]; then
    echo "Expected package not found in $HOME/.local"
    exit 1
fi

