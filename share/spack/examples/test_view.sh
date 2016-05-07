#!/bin/bash

# This will install a few bogus/test packages in order to test the
# `spack view` command.  It assumes you have "spack" in your path.

# It makes sub-directories in your CWD and installs and uninstalls
# Spack packages named test-*.

set -x
set -e

view="spack -m view -v"
for variant in +nom ~nom+var +nom+var
do
    spack -m uninstall -f -a -y test-d
    spack -m install test-d$variant
    testdir=test_view
    rm -rf $testdir
    echo "hardlink may fail if Spack install area and CWD are not same FS"
    for action in symlink hardlink
    do
	$view --dependencies=no   $action $testdir test-d
	$view -e test-a -e test-b $action $testdir test-d
	$view                     $action $testdir test-d
	$view                     status  $testdir test-d
	$view -d false            remove  $testdir test-a
	$view                     remove  $testdir test-d
	rmdir $testdir		# should not fail
    done
done
echo "Warnings about skipping existing in the above are okay"
