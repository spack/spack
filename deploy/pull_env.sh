#!/bin/sh

DEPLOYMENT_ROOT="/gpfs/bbp.cscs.ch/apps/hpc/jenkins"

usage() {
    echo "$0 pull/PR STAGE [date]"
}

pr=$1
stage=$2
date=$3

[ -z "$pr" ] && usage
[ -z "$stage" ] && usage
[ -z "$date" ] && date="latest"

tmpdir=$(mktemp -d ${PWD}/spack_${pr//\//-}_XXXXXX)
spack=$(readlink -f "${DEPLOYMENT_ROOT}/${pr}/spack")
deployment=$(readlink -f "${DEPLOYMENT_ROOT}/${pr}/deploy/${stage}/${date}")

if [ -z "${spack}" ]; then
    echo 'echo unable to find PR!'
    exit 1
fi

mkdir -p ${tmpdir}/install

cp -Rp ${deployment}/data/{.spack,spack*,*.yaml,*.txt} ${tmpdir}
cp -Rp ${deployment}/.spack-db ${tmpdir}/install

for arch in ${deployment}/*; do
    if [[ "$(basename ${arch})" = "data" ]]; then
        continue
    fi
    mkdir -p "${tmpdir}/install/$(basename ${arch})"
    for compiler in ${arch}/*; do
        mkdir -p "${tmpdir}/install/$(basename ${arch})/$(basename ${compiler})"

        for soft in ${compiler}/*; do
            ln -s "${soft}" "${tmpdir}/install/$(basename ${arch})/$(basename ${compiler})"
        done
    done
done

cat <<EOF
export SPACK_INSTALL_PREFIX=${tmpdir}/install;
export HOME=${tmpdir};
alias spacktivate="source ${spack}/share/spack/setup-env.sh";
echo "created the directory (to be deleted by the user) ${tmpdir}";
echo "use the command 'spacktivate' to source the spack of the PR";
EOF
