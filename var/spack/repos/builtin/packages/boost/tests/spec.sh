#!/bin/bash

declare failed=0

function should_fail () {
  echo -n "Testing spec '$1'..."
  if ! spack spec boost "$1" 2>&1 | grep -i "failed to concretize" >/dev/null; then
    echo "FAILED"
    failed=1
  else
    echo "OK"
  fi
}

should_fail "+beast~asio"                                             # requires asio
should_fail "+clanglibcpp %gcc"                                       # gcc doesn't support libc++
should_fail "+cobalt cxxstd=11"                                       # C++20 minimum
should_fail "+cobalt cxxstd=14"                                       # C++20 minimum
should_fail "+cobalt cxxstd=17"                                       # C++20 minimum
should_fail "+cobalt+leaf~variant2"                                   # requires variant2
should_fail "+cobalt~leaf+variant2"                                   # requires leaf
should_fail "+coroutine2~context"                                     # requires context
should_fail "+coroutine~context"                                      # requires context
should_fail "+describe cxxstd=11"                                     # C++14 minimum
should_fail "+fiber~context"                                          # requires context
should_fail "+graph_parallel+graph~mpi"                               # requires mpi
should_fail "+graph_parallel~graph+mpi"                               # requires +graph
should_fail "+hana cxxstd=11"                                         # C++14 minimum
should_fail "+histogram cxxstd=11"                                    # C++14 minimum
should_fail "+lambda2 cxxstd=11"                                      # C++14 minimum
should_fail "+locale~icu"                                             # requires icu
should_fail "+math~octonions"                                         # math requires octonions
should_fail "+math~quaternions"                                       # math requires quaternions
should_fail "+mysql+describe+pfr+variant2~asio"                       # requires asio 
should_fail "+mysql+describe+pfr~variant2+asio"                       # requires variant2
should_fail "+mysql+describe~pfr+variant2+asio"                       # requires pfr
should_fail "+mysql~describe+pfr+variant2+asio"                       # requires describe
should_fail "+numpy~python"                                           # numpy requires python
should_fail "+odeint~math"                                            # requires math
should_fail "+operators cxxstd=20"                                    # operators is broken in C++20 and beyond
should_fail "+outcome cxxstd=11"                                      # C++14 minimum
should_fail "+parameter_python~python~parameter"                      # requies python and parameter
should_fail "+parser cxxstd=11"                                       # C++17 minimum
should_fail "+parser cxxstd=14"                                       # C++17 minimum
should_fail "+pfr cxxstd=11"                                          # C++14 minimum
should_fail "+property_map_parallel+graph_parallel+property_map~mpi"  # requires mpi
should_fail "+property_map_parallel+graph_parallel~property_map+mpi"  # requires property_map
should_fail "+property_map_parallel~graph_parallel+property_map+mpi"  # requires graph_parallel
should_fail "+redis cxxstd=11"                                        # C++17 minimum
should_fail "+redis cxxstd=14"                                        # C++17 minimum
should_fail "+redis~asio cxxstd=17"                                   # requires asio
should_fail "+safe_numerics cxxstd=11"                                # C++14 minimum
should_fail "+stl_interfaces cxxstd=11"                               # C++14 minimum
should_fail "+url~variant2"                                           # requires variant2
should_fail "+vmd~preprocessor"                                       # requires preprocessor
should_fail "+yap cxxstd=11"                                          # C++14 minimum
should_fail "@1.62.0 cxxstd=17"                                       # 1.63.0 added C++17 support
should_fail "@1.71.0 +histogram ~variant2"                            # 1.71.0 added dependency on variant2
should_fail "@1.72.0 +mpi cxxstd=98"                                  # mpi@1.72.0 does not support C++98
should_fail "@1.72.0+clanglibcpp"                                     # introduced in 1.73.0
should_fail "@1.73.0 cxxstd=2a"                                       # 1.73.0 added C++2a support
should_fail "@1.75.0 +geometry cxxstd=11"                             # 1.75.0 made C++14 minimum
should_fail "@1.75.0 +lexical_cast~math"                              # 1.76.0 removed dependency on math
should_fail "@1.76.0 +math cxxstd=03"                                 # 1.76.0 made C++11 minimum
should_fail "@1.76.0 +multiprecision cxxstd=03"                       # 1.76.0 made C++11 minimum
should_fail "@1.76.0 cxxstd=20"                                       # 1.77.0 added C++20 support
should_fail "@1.78.0 cxxstd=23"                                       # 1.79.0 added C++23 support
should_fail "@1.78.0 cxxstd=26"                                       # 1.79.0 added C++26 support
should_fail "@1.80.0 +asio cxxstd=03"                                 # 1.80.0 made C++11 minimum
should_fail "@1.80.0 +asio~context"                                   # 1.80.0 added dependency on context
should_fail "@1.80.0 +gil cxxstd=11"                                  # 1.80.0 made C++14 minimum
should_fail "@1.81.0 cxxstd=03"                                       # 1.81.0 made C++11 minimum
should_fail "@1.82.0 +math cxxstd=11"                                 # 1.82.0 made C++14 minimum
should_fail "@1.82.0 +multiprecision cxxstd=11"                       # 1.82.0 made C++14 minimum
should_fail "@1.84.0 +log ~regex"                                     # 1.84.0 added dependency on regex
should_fail "@1.84.0 cxxstd=03"                                       # 1.84.0 removed C++98 support
should_fail "@1.84.0 cxxstd=98"                                       # 1.84.0 removed C++98 support
should_fail "@1.85.0 +clanglibcpp+stacktrace"                         # 1.85.0 stacktrace added a hard compilation error
should_fail "@1.85.0 +graph cxxstd=11"                                # 1.85.0 made C++14 minimum
should_fail "@1.85.0 +json~endian"                                    # 1.85.0 added dependency on endian
should_fail "@1.85.0 +uuid cxxstd=03"                                 # 1.86.0 made C++11 minimum
should_fail "@1.85.0 +mysql+describe+pfr+variant2+asio~charconv"      # 1.85.0 added dependency on charconv
should_fail "@1.86.0 +graph~regex"                                    # 1.86.0 added dependency on regex
should_fail "@1.87.0 +mpi~python"                                     # 1.87.0 requires python


exit $failed
