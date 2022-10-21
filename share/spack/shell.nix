{ pkgs ? (import <nixpkgs> {}) }:

with pkgs; stdenv.mkDerivation {

  buildInputs = [
    python3
    gnupg

    # fortran compiler not exposed by standard environment
    gfortran
    gfortran.cc.lib
  ];

  name = "spack-shell";
  shellHook = "source ./setup-env.sh";
}
