# a simple CXX only test case
cmake_minimum_required(VERSION 3.10)
project (SimpleSmokeTest CXX)

add_executable (smoke1 add.cxx)

install (TARGETS smoke1 DESTINATION bin)

