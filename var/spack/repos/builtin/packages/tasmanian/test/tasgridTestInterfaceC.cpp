/*
 * Copyright (c) 2017, Miroslav Stoyanov
 *
 * This file is part of
 * Toolkit for Adaptive Stochastic Modeling And Non-Intrusive ApproximatioN: TASMANIAN
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
 *    and the following disclaimer in the documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
 *    or promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
 * OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * UT-BATTELLE, LLC AND THE UNITED STATES GOVERNMENT MAKE NO REPRESENTATIONS AND DISCLAIM ALL WARRANTIES, BOTH EXPRESSED AND IMPLIED.
 * THERE ARE NO EXPRESS OR IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY PATENT,
 * COPYRIGHT, TRADEMARK, OR OTHER PROPRIETARY RIGHTS, OR THAT THE SOFTWARE WILL ACCOMPLISH THE INTENDED RESULTS OR THAT THE SOFTWARE OR ITS USE WILL NOT RESULT IN INJURY OR DAMAGE.
 * THE USER ASSUMES RESPONSIBILITY FOR ALL LIABILITIES, PENALTIES, FINES, CLAIMS, CAUSES OF ACTION, AND COSTS AND EXPENSES, CAUSED BY, RESULTING FROM OR ARISING OUT OF,
 * IN WHOLE OR IN PART THE USE, STORAGE OR DISPOSAL OF THE SOFTWARE.
 */

extern "C"{

#include "stdio.h"
#include "stdlib.h"
#include "math.h"
#include "TasmanianSparseGrid.h"

// The bulk of the C interface is tested through the Python wrapper
// The purpose of this function is to test the C header and the few untested functions
int testInterfaceC(){

    void *grid = tsgConstructTasmanianSparseGrid();
    if (tsgGetPoints(grid) != 0){ printf("ERROR: empty grid did not return null pointer on tsgGetPoints()\n"); return 0; }
    tsgMakeGlobalGrid(grid, 2, 1, 1, "level", "clenshaw-curtis", 0, 0.0, 0.0, 0, 0);
    int num_points = tsgGetNumPoints(grid);
    if (num_points != 5){
        printf("ERROR: simple Clenshaw-Curtis grid doesn't have 5 points.");
        return 0;
    }

    if (tsgGetLoadedPoints(grid) != 0){ printf("ERROR: empty grid did not return null pointer on tsgGetLoadedPoints()\n"); return 0; }
    double tpoints[10] = {0.0, 0.0, 0.0, -1.0, 0.0, 1.0, -1.0, 0.0, 1.0, 0.0};
    double *points = tsgGetPoints(grid);
    int i, j;
    for(i=0; i<10; i++) if (fabs(points[i] - tpoints[i]) > 1.E-15){ printf("ERROR: mismatch in points i = %d, expected = %1.16e, actual = %1.16e\n",i,tpoints[i],points[i]); return 0; }
    free(points);

    points = tsgGetNeededPoints(grid);
    for(i=0; i<10; i++) if (fabs(points[i] - tpoints[i]) > 1.E-15){ printf("ERROR: mismatch in needed points i = %d, expected = %1.16e, actual = %1.16e\n",i,tpoints[i],points[i]); return 0; }
    free(points);

    double values[5] = {0.0, 1.0, 1.0, 1.0, 1.0};
    tsgLoadNeededPoints(grid, values);

    if (tsgGetNeededPoints(grid) != 0){ printf("ERROR: empty grid did not return null pointer on tsgGetNeededPoints()\n"); return 0; }
    points = tsgGetLoadedPoints(grid);
    for(i=0; i<10; i++) if (fabs(points[i] - tpoints[i]) > 1.E-15){ printf("ERROR: mismatch in loaded points i = %d, expected = %1.16e, actual = %1.16e\n",i,tpoints[i],points[i]); return 0; }
    free(points);

    double tweights[5] = {4.0/3.0, 2.0/3.0, 2.0/3.0, 2.0/3.0, 2.0/3.0};
    double *weights = tsgGetQuadratureWeights(grid);
    for(i=0; i<5; i++) if (fabs(weights[i] - tweights[i]) > 1.E-15){ printf("ERROR: mismatch quadrature i = %d, expected = %1.16e, actual = %1.16e\n",i,tweights[i],weights[i]); return 0; }
    free(weights);

    double x[2] = {0.0, 1.0};
    double tiweights[5] = {0.0, 0.0, 1.0, 0.0, 0.0};
    weights = tsgGetInterpolationWeights(grid, x);
    for(i=0; i<5; i++) if (fabs(weights[i] - tiweights[i]) > 1.E-15){ printf("ERROR: mismatch iweights i = %d, expected = %1.16e, actual = %1.16e\n",i,tiweights[i],weights[i]); return 0; }
    free(weights);

    int n = tsgGetNumPoints(grid);
    points = tsgGetPoints(grid);
    weights = tsgBatchGetInterpolationWeights(grid, points, n);
    for(i=0; i<n; i++){
        for(j=0; j<n; j++){
            double expect = (i == j) ? 1.0 : 0.0;
            if (fabs(weights[i*n + j] - expect) > 1.E-15){ printf("ERROR: mismatch batch iweights i = %d, expected = %1.16e, actual = %1.16e\n",i,expect,weights[i]); return 0; }
        }
    }
    free(weights);
    free(points);

    int tcoeffs[4];
    tsgEstimateAnisotropicCoefficientsStatic(grid, "ipcurved", 0, tcoeffs);
    int *coeffs = tsgEstimateAnisotropicCoefficients(grid, "ipcurved", 0, &n);
    if (n != 4){ printf("ERROR: mismatch in number of anisotropic coefficients\n"); return 0; }
    for(i=0; i<n; i++) if (coeffs[i] != tcoeffs[i]){ printf("ERROR: mismatch acoeffs i = %d, expected = %d, actual = %d\n",i,tcoeffs[i],coeffs[i]); return 0; }
    free(coeffs);

    tsgDestructTasmanianSparseGrid(grid);

    char name[256];
    int num_char;
    tsgGetGPUName(0, 256, name, &num_char); // checks for memory leaks

    // check tsgEvaluateSparseHierarchicalFunctions()
    grid = tsgConstructTasmanianSparseGrid();
    tsgMakeLocalPolynomialGrid(grid, 4, 1, 5, 1, "localp", 0);
    double *pnts = tsgGetPoints(grid);
    int nump = tsgGetNumPoints(grid);
    double *model = (double*) malloc(nump * sizeof(double));
    for(i=0; i<nump; i++)
        model[i] = exp(pnts[4*i] + pnts[4*i+1] + pnts[4*i+2] + pnts[4*i+3]);
    tsgLoadNeededPoints(grid, model);

    int numx = 10;
    double *x2 = (double*) malloc(4 * numx * sizeof(double));
    for(i=0; i<4 * numx; i++)
        x2[i] = 1.0 / (1.0 + (double) i);
    double *internal_result = (double*) malloc(numx * sizeof(double));
    tsgEvaluateBatch(grid, x2, numx, internal_result);

    double *external_result = (double*) malloc(numx * sizeof(double));
    int *pntr, *indx;
    double *vals;
    const double *coeff = tsgGetHierarchicalCoefficients(grid);
    tsgEvaluateSparseHierarchicalFunctions(grid, x2, numx, &pntr, &indx, &vals);

    for(i=0; i<numx; i++){
        double sum = 0.0;
        for(j=pntr[i]; j<pntr[i+1]; j++)
            sum += vals[j] * coeff[indx[j]];
        external_result[i] = sum;
    }

    double err = 0.0;
    for(i=0; i<numx; i++) if (fabs(external_result[i] - internal_result[i]) > err) err = fabs(external_result[i] - internal_result[i]);
    if (err > 1.E-13){ printf("ERROR: mismatch in external and internal sparse hierarchical matrix.\n"); return 0; }

    free(pntr);
    free(indx);
    free(vals);
    free(external_result);
    free(internal_result);
    free(model);
    free(pnts);
    free(x2);

    tsgDestructTasmanianSparseGrid(grid);

    // test global polynomial space
    grid = tsgConstructTasmanianSparseGrid();
    tsgMakeGlobalGrid(grid, 2, 1, 1, "level", "clenshaw-curtis", 0, 0.0, 0.0, 0, 0);
    int *pspace;
    int tspace[10] = {0, 0, 0, 1, 0, 2, 1, 0, 2, 0};
    tsgGetGlobalPolynomialSpace(grid, 1, &n, &pspace);
    if (n != 5){ printf("ERROR: mismatch in size of the interpolated polynomial space.\n"); return 0; }
    for(i=0; i<10; i++) if (pspace[i] != tspace[i]){ printf("ERROR: mismatch in polynomial space i = %d, expected = %d, actual = %d\n",i,tspace[i],pspace[i]); return 0; }

    free(pspace);
    tsgDestructTasmanianSparseGrid(grid);

    grid = tsgConstructTasmanianSparseGrid();
    void* grid_copy = tsgConstructTasmanianSparseGrid();
    tsgMakeGlobalGrid(grid, 2, 1, 1, "level", "fejer2", 0, 0.0, 0.0, 0, 0);
    tsgCopyGrid(grid_copy, grid);
    double *quad1 = tsgGetQuadratureWeights(grid);
    double *quad2 = tsgGetQuadratureWeights(grid_copy);
    for(i=0; i<tsgGetNumPoints(grid); i++) if (fabs(quad1[i] - quad2[i]) > 1.E-15){ printf("ERROR: mismatch in quadrature after copy.\n"); return 0; }
    free(quad1);
    free(quad2);
    tsgDestructTasmanianSparseGrid(grid);
    tsgDestructTasmanianSparseGrid(grid_copy);

    return 1;
}


}
