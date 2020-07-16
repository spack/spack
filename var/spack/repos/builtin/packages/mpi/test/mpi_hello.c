#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv){
  MPI_Init(argc, argv);

  int rank;
  int num_ranks;
  MPI_Comm_size(MPI_COMM_WORLD, &num_ranks);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  printf("Hello world! From rank %s of %s\n", rank, num_ranks);

  MPI_Finalize();
}
