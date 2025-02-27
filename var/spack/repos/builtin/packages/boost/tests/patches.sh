#!/bin/bash

declare failed=0

function test_patch () {
  echo -n "Patching '$1'..."
  if spack patch boost "$1" >/dev/null 2>&1; then
    echo "OK"
  else
    echo "FAILED"
    failed=1
  fi
}

test_patch "@1.54.0 +python ^python@3"        # python_jam_pre156, glibc_gentoo_v1.53.0.patch, thread_svn10125
test_patch "@1.55.0 %clang"                   # clang-linux_add_option2
test_patch "@1.56.0 %clang"                   # clang-linux_add_option, build_PR154
test_patch "@1.63.0 +python +numpy"           # python_PR218, python_PR432
test_patch "@1.69.0 +system"                  # system-non-virtual-dtor-{include,test}, pthread-stack-min-fix
test_patch "@1.72.0 +process"                 # process_PR116
test_patch "@1.73.0 +beast +outcome"          # beast_PR1927, outcome_PR223
test_patch "@1.75"                            # bootstrap-toolset
test_patch "@1.76.0 +python ^python@3"        # python_jam, bootstrap-compiler
test_patch "@1.77.0 +python ^python@3"        # python_jam-1_77, b2_PR79
test_patch "@1.78.0 +atomic"                  # build_1780_PR113, atomic_1780_PR54
test_patch "@1.79.0 +json"                    # json_PR695
test_patch "@1.80.0 +filesystem +unordered"   # filesystem_PR250, unordered_PR139
test_patch "@1.81.0 +phoenix"                 # phoenix_PR111
test_patch "@1.82.0 +filesystem"              # filesystem_PR283
test_patch "@1.83.0 +json +unordered"         # json_PR926, unordered_PR205
test_patch "@1.85.0 +container"               # container_PR273
test_patch "@1.87.0 +context"                 # context_impl_module

exit $failed
