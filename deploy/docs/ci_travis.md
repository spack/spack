# Using Spack for Continuous Integration with Travis

The [MVDTool CI configuration](https://github.com/BlueBrain/MVDTool/blob/master/.travis.yml) shows how to use our continuously updated Docker image with Travis for a simple build:

    services:
      - docker

    matrix:
      include:
      - name: "C++ Build"
        before_install:
          - docker pull bluebrain/spack
          - docker run -v $PWD:/source -w /source bluebrain/spack:latest spack diy --test=root mvdtool@develop
      - name: "Python Build"
        before_install:
          - docker pull bluebrain/spack
          - docker run -v $PWD:/source -w /source bluebrain/spack:latest spack diy --test=root "py-mvdtool@develop^python@3:"

    script: "ruby -ne 'puts $_ if /^==>.*make.*test|^==>.*python.*setup\\.py.*test/../.*phase.*install/ and not /^==>|make: \\*\\*\\*/' spack-build.out"

The last line will extract the results from running unit tests during
installation for your convenience.  This requires either a valid test
target for `make` in CMake or a corresponding command in `setup.py` for
Python.
