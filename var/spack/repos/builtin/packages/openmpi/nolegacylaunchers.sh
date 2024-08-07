#!/bin/sh
cat <<_EOF >&2
error: '$0' is disabled in this MPI installation.
Please refer to your site's user guide for the recommended way to launch MPI
applications.

_EOF
exit 2
