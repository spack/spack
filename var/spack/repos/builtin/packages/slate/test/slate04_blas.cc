// example_04.cc
// BLAS routines
#include <slate/slate.hh>

#include "util.hh"

int mpi_size = 0;
int mpi_rank = 0;

//------------------------------------------------------------------------------
template <typename scalar_type>
void test_gemm()
{
    print_func( mpi_rank );

    double alpha = 2.0, beta = 1.0;
    int64_t m=2000, n=1000, k=500, nb=256, p=2, q=2;
    assert( mpi_size == p*q );
    slate::Matrix<double> A( m, k, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B( k, n, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> C( m, n, nb, p, q, MPI_COMM_WORLD );
    A.insertLocalTiles();
    B.insertLocalTiles();
    C.insertLocalTiles();
    random_matrix( A );
    random_matrix( B );
    random_matrix( C );

    // C = alpha A B + beta C
    slate::multiply( alpha, A, B, beta, C );  // simplified API

    slate::gemm( alpha, A, B, beta, C );      // traditional API

    //--------------------
    // with options
    // slate::gemm( alpha, A, B, beta, C, {
    //     { slate::Option::Lookahead, 1 },
    //     { slate::Option::Target, slate::Target::Devices },  // on GPU devices
    // } );
}

//------------------------------------------------------------------------------
template <typename scalar_type>
void test_gemm_transpose()
{
    print_func( mpi_rank );

    double alpha = 2.0, beta = 1.0;
    int64_t m=2000, n=1000, k=500, nb=256, p=2, q=2;
    assert( mpi_size == p*q );
    // Dimensions of X, Y, Z are backwards from A, B, C in test_gemm().
    slate::Matrix<double> X( k, m, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> Y( n, k, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> Z( m, n, nb, p, q, MPI_COMM_WORLD );
    X.insertLocalTiles();
    Y.insertLocalTiles();
    Z.insertLocalTiles();
    random_matrix( X );
    random_matrix( Y );
    random_matrix( Z );

    // Z = alpha X^T Y^H + beta Z
    auto XT = transpose( X );
    auto YH = conj_transpose( Y );
    slate::multiply( alpha, XT, YH, beta, Z );  // simplified API

    slate::gemm( alpha, XT, YH, beta, Z );      // traditional API

    // todo: support rvalues:
    // slate::gemm( alpha, transpose( X ), conj_transpose( Y ), beta, C );
    // or
    // slate::gemm( alpha, transpose( X ), conj_transpose( Y ), beta, std::move( C ) );
}

//------------------------------------------------------------------------------
template <typename scalar_type>
void test_symm()
{
    print_func( mpi_rank );

    double alpha = 2.0, beta = 1.0;
    int64_t m=2000, n=1000, nb=256, p=2, q=2;
    assert( mpi_size == p*q );
    slate::SymmetricMatrix<double>
        A( slate::Uplo::Lower, m, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B1( m, n, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B2( n, m, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> C1( m, n, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> C2( n, m, nb, p, q, MPI_COMM_WORLD );
    A.insertLocalTiles();
    B1.insertLocalTiles();
    B2.insertLocalTiles();
    C1.insertLocalTiles();
    C2.insertLocalTiles();
    random_matrix( A );
    random_matrix( B1 );
    random_matrix( B2 );
    random_matrix( C1 );
    random_matrix( C2 );

    //----- left
    // C1 = alpha A B1 + beta C1, where A is symmetric
    slate::multiply( alpha, A, B1, beta, C1 );                  // simplified API

    slate::symm( slate::Side::Left, alpha, A, B1, beta, C1 );   // traditional API

    //----- right
    // C2 = alpha B2 A + beta C2, where A is symmetric
    slate::multiply( alpha, B2, A, beta, C2 );                  // simplified API

    slate::symm( slate::Side::Right, alpha, A, B2, beta, C2 );  // traditional API
}

//------------------------------------------------------------------------------
template <typename scalar_type>
void test_syrk_syr2k()
{
    print_func( mpi_rank );

    double alpha = 2.0, beta = 1.0;
    int64_t n=1000, k=500, nb=256, p=2, q=2;
    assert( mpi_size == p*q );
    slate::Matrix<double> A( n, k, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B( n, k, nb, p, q, MPI_COMM_WORLD );
    slate::SymmetricMatrix<double>
        C( slate::Uplo::Lower, n, nb, p, q, MPI_COMM_WORLD );
    A.insertLocalTiles();
    B.insertLocalTiles();
    C.insertLocalTiles();
    random_matrix( A );
    random_matrix( B );
    random_matrix( C );

    // C = alpha A A^T + beta C
    slate::rank_k_update( alpha, A, beta, C );      // simplified API

    slate::syrk( alpha, A, beta, C );               // traditional API

    // C = alpha A B^T + alpha B A^T + beta C
    slate::rank_2k_update( alpha, A, B, beta, C );  // simplified API

    slate::syr2k( alpha, A, B, beta, C );           // traditional API
}

//------------------------------------------------------------------------------
template <typename scalar_type>
void test_trmm_trsm()
{
    print_func( mpi_rank );

    double alpha = 2.0;
    int64_t m=2000, n=1000, nb=256, p=2, q=2;
    assert( mpi_size == p*q );
    slate::TriangularMatrix<double>
        A( slate::Uplo::Lower, slate::Diag::NonUnit, m, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B1( m, n, nb, p, q, MPI_COMM_WORLD );
    slate::Matrix<double> B2( n, m, nb, p, q, MPI_COMM_WORLD );
    A.insertLocalTiles();
    B1.insertLocalTiles();
    B2.insertLocalTiles();
    random_matrix( A );
    random_matrix( B1 );
    random_matrix( B2 );

    //----- left
    // B1 = alpha A B1, where A is triangular
    slate::triangular_multiply( alpha, A, B1 );       // simplified API

    slate::trmm( slate::Side::Left, alpha, A, B1 );   // traditional API

    // B1 = alpha A^{-1} B1, where A is triangular
    slate::triangular_solve( alpha, A, B1 );          // simplified API

    slate::trsm( slate::Side::Left, alpha, A, B1 );   // traditional API

    //----- right
    // B2 = alpha B2 A, where A is triangular
    slate::triangular_multiply( alpha, B2, A );       // simplified API

    slate::trmm( slate::Side::Right, alpha, A, B2 );  // traditional API

    // B2 = alpha B2 A^{-1}, where A is triangular
    slate::triangular_solve( alpha, B2, A );          // simplified API

    slate::trsm( slate::Side::Right, alpha, A, B2 );  // traditional API
}

//------------------------------------------------------------------------------
int main( int argc, char** argv )
{
    int provided = 0;
    int err = MPI_Init_thread( &argc, &argv, MPI_THREAD_MULTIPLE, &provided );
    assert( err == 0 );
    assert( provided == MPI_THREAD_MULTIPLE );

    err = MPI_Comm_size( MPI_COMM_WORLD, &mpi_size );
    assert( err == 0 );
    if (mpi_size != 4) {
        printf( "Usage: mpirun -np 4 %s  # 4 ranks hard coded\n", argv[0] );
        return -1;
    }

    err = MPI_Comm_rank( MPI_COMM_WORLD, &mpi_rank );
    assert( err == 0 );

    // so random_matrix is different on different ranks.
    srand( 100 * mpi_rank );

    test_gemm< float >();
    test_gemm< double >();
    test_gemm< std::complex<float> >();
    test_gemm< std::complex<double> >();

    test_gemm_transpose< float >();
    test_gemm_transpose< double >();
    test_gemm_transpose< std::complex<float> >();
    test_gemm_transpose< std::complex<double> >();

    test_symm< float >();
    test_symm< double >();
    test_symm< std::complex<float> >();
    test_symm< std::complex<double> >();

    test_syrk_syr2k< float >();
    test_syrk_syr2k< double >();
    test_syrk_syr2k< std::complex<float> >();
    test_syrk_syr2k< std::complex<double> >();

    test_trmm_trsm< float >();
    test_trmm_trsm< double >();
    test_trmm_trsm< std::complex<float> >();
    test_trmm_trsm< std::complex<double> >();

    err = MPI_Finalize();
    assert( err == 0 );
}
