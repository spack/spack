# Tests that Spack ignores directories without a Ninja build script

cflags = -Wall

rule cc
  command = gcc $cflags -c $in -o $out

build check: cc foo.c
