#!/bin/bash


# spack test command
"spack" "-d" "-v" "test" "run" "--cdash-upload-url" "file://fake/submit.php?project=ci-unit-testing" "--cdash-build" "ci-test-build" "--cdash-site" "fake-site (test-runner)" "--cdash-buildstamp" "ci-test-build-stamp" "printing-package"
