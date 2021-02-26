#ifndef UTIL_H
#define UTIL_H

#include <blas.hh>
#include <stdio.h>

//------------------------------------------------------------------------------
void print_func_( int rank, const char* func )
{
    printf( "rank %d: %s\n", rank, func );
}

#ifdef __GNUC__
    #define print_func( rank ) print_func_( rank, __PRETTY_FUNCTION__ )
#else
    #define print_func( rank ) print_func_( rank, __func__ )
#endif

//------------------------------------------------------------------------------
// utility to create real or complex number
template <typename scalar_type>
scalar_type make( blas::real_type<scalar_type> re,
                  blas::real_type<scalar_type> im )
{
    return re;
}

template <typename T>
std::complex<T> make( T re, T im )
{
    return std::complex<T>( re, im );
}

//------------------------------------------------------------------------------
// generate random matrix A
template <typename scalar_type>
void random_matrix( int64_t m, int64_t n, scalar_type* A, int64_t lda )
{
    for (int64_t j = 0; j < n; ++j) {
        for (int64_t i = 0; i < m; ++i) {
            A[ i + j*lda ] = make<scalar_type>( rand() / double(RAND_MAX),
                                                rand() / double(RAND_MAX) );
        }
    }
}

//------------------------------------------------------------------------------
// generate random, diagonally dominant matrix A
template <typename scalar_type>
void random_matrix_diag_dominant( int64_t m, int64_t n, scalar_type* A, int64_t lda )
{
    using blas::real;
    int64_t max_mn = std::max( m, n );
    for (int64_t j = 0; j < n; ++j) {
        for (int64_t i = 0; i < m; ++i) {
            A[ i + j*lda ] = make<scalar_type>( rand() / double(RAND_MAX),
                                                rand() / double(RAND_MAX) );
        }
        if (j < m) {
            // make diagonal real & dominant
            A[ j + j*lda ] = real( A[ j + j*lda ] ) + max_mn;
        }
    }
}

//------------------------------------------------------------------------------
// generate random matrix A
template <typename matrix_type>
void random_matrix( matrix_type& A )
{
    for (int64_t j = 0; j < A.nt(); ++j) {
        for (int64_t i = 0; i < A.mt(); ++i) {
            if (A.tileIsLocal( i, j )) {
                try {
                    auto T = A( i, j );
                    random_matrix( T.mb(), T.nb(), T.data(), T.stride() );
                }
                catch (...) {
                    // ignore missing tiles
                }
            }
        }
    }
}

//------------------------------------------------------------------------------
// generate random, diagonally dominant matrix A
template <typename matrix_type>
void random_matrix_diag_dominant( matrix_type& A )
{
    using blas::real;
    int64_t max_mn = std::max( A.m(), A.n() );
    for (int64_t j = 0; j < A.nt(); ++j) {
        for (int64_t i = 0; i < A.mt(); ++i) {
            if (A.tileIsLocal( i, j )) {
                try {
                    auto T = A( i, j );
                    random_matrix( T.mb(), T.nb(), T.data(), T.stride() );
                    if (i == j) {
                        // assuming tileMb == tileNb, then i == j are diagonal tiles
                        // make diagonal real & dominant
                        int64_t min_mb_nb = std::min( T.mb(), T.nb() );
                        for (int64_t ii = 0; ii < min_mb_nb; ++ii) {
                            T.at(ii, ii) = real( T.at(ii, ii) ) + max_mn;
                        }
                    }
                }
                catch (...) {
                    // ignore missing tiles
                }
            }
        }
    }
}

//------------------------------------------------------------------------------
template <typename scalar_type>
void print_matrix( const char* label, int m, int n, scalar_type* A, int lda )
{
    using blas::real;
    using blas::imag;
    printf( "%s = [\n", label );
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (blas::is_complex<scalar_type>::value) {
                printf( "  %7.4f + %7.4fi", real(A[ i + j*lda ]), imag(A[ i + j*lda ]) );
            }
            else {
                printf( "  %7.4f", real(A[ i + j*lda ]) );
            }
        }
        printf( "\n" );
    }
    printf( "];\n" );
}

//------------------------------------------------------------------------------
// suppress compiler "unused" warning for variable x
#define unused( x ) ((void) x)

#endif // UTIL_H
