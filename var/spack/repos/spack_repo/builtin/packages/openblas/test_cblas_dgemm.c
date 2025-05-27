#include <cblas.h>
#include <stdio.h>

double m[] = {
  3, 1, 3,
  1, 5, 9,
  2, 6, 5
};

double x[] = {
  -1, 3, -3
};

#ifdef __cplusplus
extern "C" {
#endif

     void dgesv_(int *n, int *nrhs,  double *a,  int  *lda,
           int *ipivot, double *b, int *ldb, int *info);

#ifdef __cplusplus
}
#endif

int main(void) {
  int i;
  // blas:
  double A[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
  double B[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
  double C[9] = {.5, .5, .5, .5, .5, .5, .5, .5, .5};
  cblas_dgemm(CblasColMajor, CblasNoTrans, CblasTrans,
              3, 3, 2, 1, A, 3, B, 3, 2, C, 3);
  for (i = 0; i < 9; i++)
    printf("%f\n", C[i]);

  // lapack:
  int ipiv[3];
  int j;
  int info;
  int n = 1;
  int nrhs = 1;
  int lda = 3;
  int ldb = 3;
  dgesv_(&n,&nrhs, &m[0], &lda, ipiv, &x[0], &ldb, &info);
  for (i=0; i<3; ++i)
    printf("%5.1f\n", x[i]);

  return 0;
}
