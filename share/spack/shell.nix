{ pkgs ? (import <nixpkgs> {}),
  stdenv ? pkgs.stdenv
}:

stdenv.mkDerivation {

  buildInputs = with pkgs; [
    python3
    gnupg

    # fortran compiler not exposed by standard environment
    gfortran
    gfortran.cc.lib
  ];

  name = "spack-shell";
  shellHook = "source ./setup-env.sh";
}
