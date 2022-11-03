static char help[] = "Hello World example program\n";

#include "slepcsys.h"

int main( int argc, char **argv )
{
  int ierr;

  SlepcInitialize(&argc,&argv,(char*)0,help);
  ierr = PetscPrintf(PETSC_COMM_WORLD,"Hello world\n");

  return ierr;
}

