{ pkgs ? (import <nixpkgs> {}),
  stdenv ? pkgs.stdenv
}:

stdenv.mkDerivation {

  buildInputs = with pkgs; [
    python3
    gnupg
    gfortran
  ];

  name = "spack-shell";
  shellHook = "source ./setup-env.sh";
}
