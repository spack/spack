c Fortran example
      program hello
      include 'mpif.h'
      integer rank, num_ranks, err_flag

      call MPI_INIT(err_flag)
      call MPI_COMM_SIZE(MPI_COMM_WORLD, num_ranks, err_flag)
      call MPI_COMM_RANK(MPI_COMM_WORLD, rank, err_flag)
      print*, 'Hello world! From rank', rank, 'of ', num_ranks
      call MPI_FINALIZE(err_flag)
      end
