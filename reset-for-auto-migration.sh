#!/bin/bash
# Reset Spack state to force auto-migration to run again
#
# This removes:
# - ~/.config/spack/ (new user config location)
# - ~/.local/share/spack/ (new data location - licenses, environments, etc.)
# - ~/.local/state/spack/ (new state location - bootstrap, repos, etc.)
# - etc/spack/isolate/ (isolate scope)
# - etc/spack/layout/ (layout scope - contains config overrides for non-migrated resources)
# - .migration-done (migration completion marker in $spack prefix)
#
# Old resources (var/environments, etc/spack/gpg, etc/spack/licenses) are left in place
# since migration copies them rather than moving them.
#
# After running this, the next spack command will trigger auto-migration.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Removing Spack configuration to force re-migration..."

if [ -d "$HOME/.config/spack" ]; then
    echo "  Removing $HOME/.config/spack/"
    rm -rf "$HOME/.config/spack/"
fi

if [ -d "$HOME/.local/share/spack" ]; then
    echo "  Removing $HOME/.local/share/spack/"
    rm -rf "$HOME/.local/share/spack/"
fi

if [ -d "$HOME/.local/state/spack" ]; then
    echo "  Removing $HOME/.local/state/spack/"
    rm -rf "$HOME/.local/state/spack/"
fi

if [ -d "$SCRIPT_DIR/etc/spack/isolate" ]; then
    echo "  Removing $SCRIPT_DIR/etc/spack/isolate/"
    rm -rf "$SCRIPT_DIR/etc/spack/isolate/"
fi

if [ -d "$SCRIPT_DIR/etc/spack/layout" ]; then
    echo "  Removing $SCRIPT_DIR/etc/spack/layout/"
    rm -rf "$SCRIPT_DIR/etc/spack/layout/"
fi

if [ -f "$SCRIPT_DIR/.migration-done" ]; then
    echo "  Removing $SCRIPT_DIR/.migration-done"
    rm -f "$SCRIPT_DIR/.migration-done"
fi

if [ -f "$SCRIPT_DIR/.migration-lock" ]; then
    echo "  Removing $SCRIPT_DIR/.migration-lock (if stale)"
    rm -f "$SCRIPT_DIR/.migration-lock"
fi

echo "Done. Next spack command will trigger auto-migration."
echo "Old resources remain at their original locations and will be re-copied."
