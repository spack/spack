# command: nix-shell
#   create a spack environment built ontop of the default nix standard environment

# command: nix-shell --arg stdenv "(import <nixpkgs> {}).llvmPackages_latest.stdenv"
#   create a spack environment built ontop of a clang based nix standard environment

{ pkgs ? (import <nixpkgs> {}),
  stdenv ? (import <nixpkgs> {}).stdenv
}:

stdenv.mkDerivation {
  buildInputs = with pkgs; [
    python3
    gnupg
  ];
  name = "spack-shell";
  shellHook = "source ./setup-env.sh";
}
