#! /bin/bash
SCRIPTDIR=`dirname "${BASH_SOURCE[0]}"`
pushd ${SCRIPTDIR}
SCRIPTDIR=`pwd`
popd

source ${SCRIPTDIR}/sorttestshort.sh

sorttestshort | bamsort | bamchecksort

# copy pipe return status array
PIPESTAT=( ${PIPESTATUS[*]} )

if [ ${PIPESTAT[0]} -ne 0 ] ; then
	echo 'bamsort failed'
	exit 1
elif [ ${PIPESTAT[1]} -ne 0 ] ; then
	echo 'bamchecksort failed'
	exit 1
fi

exit 0
