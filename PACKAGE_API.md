# Package API v1.1

**Simplified form for virtuals on edges**

Virtuals on edges can now be written omitting the `virtuals=` preamble
within `[]` brackets. This makes the following specs:
```
hdf5 ^[virtuals=mpi] mpich
hdf5 ^[virtuals=lapack,blas] openblas 
```
equivalent to the shorter form:
```
hdf5 ^[mpi] mpich
hdf5 ^[lapack,blas] openblas 
```

