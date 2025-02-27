#!/bin/bash

declare build_jobs=16

declare failed=0
declare test_num=0

function test_install () {
  echo -n "Installing '$1'..."
  ((test_num++))
  declare log_file="build-${test_num}.log"
  if spack install -v -j ${build_jobs} boost "$1" >${log_file} 2>&1; then
    echo "OK"
    spack uninstall -y boost "$1" >/dev/null 2>&1
    rm -f ${log_file}
  else
    echo "FAILED"
    failed=1
  fi
}

test_install ""
test_install "%gcc"
test_install "@develop %gcc"
test_install "@develop %clang"
test_install "+clanglibcpp~stacktrace %clang"

# Layouts (can only be one type)
for l in "+versionedlayout" "+taggedlayout"; do
  # non-default build options
  test_install "+debug+icu+singlethreaded+$l"
done

# All python stuff
python_libs="+python+numpy+parameter_python+parameter"
test_install "${python_libs} ^py-numpy@1"
test_install "${python_libs} ^py-numpy@2"

# All mpi/parallel stuff
parallel="+graph_parallel+property_map_parallel+mpi"
test_install ${parallel}

# All non-parallel, non-windows, non-default libraries
# 'operators' is broken in C++20
non_default="+locale+icu+parser+cobalt+leaf+variant2+redis+asio~operators cxxstd=20"
test_install "${non_default}"

# Big build
test_install "${python_libs}${parallel}${non_default}"

# ICU support for Regex
test_install "+regex+icu"


exit $failed
