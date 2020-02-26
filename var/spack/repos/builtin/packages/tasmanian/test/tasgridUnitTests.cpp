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

#ifndef __TASGRID_UNIT_TESTS_CPP
#define __TASGRID_UNIT_TESTS_CPP

#include "tasgridUnitTests.hpp"
#include "tasgridExternalTests.hpp"

void gridLoadEN2(TasmanianSparseGrid *grid){ // load points using model exp( - \| x \|^2 )
    std::vector<double> points;
    grid->getNeededPoints(points);
    int dims = grid->getNumDimensions();
    int outs = grid->getNumOutputs();
    int nump = grid->getNumNeeded();
    std::vector<double> vals(((size_t) nump) * ((size_t) outs));
    auto iter_x = points.begin();
    auto iter_y = vals.begin();
    while(iter_x < points.end()){
        double nrm = 0.0;
        for(int i=0; i<dims; i++){
            nrm += *iter_x * *iter_x;
            iter_x++;
        }
        nrm = std::exp(-nrm);
        for(int i=0; i<outs; i++) *iter_y++ = nrm;
    }
    grid->loadNeededPoints(vals);
}

GridUnitTester::GridUnitTester() : verbose(false){}
GridUnitTester::~GridUnitTester(){}

void GridUnitTester::setVerbose(bool new_verbose){ verbose = new_verbose; }

UnitTests GridUnitTester::hasTest(std::string const &s){
    std::map<std::string, UnitTests> string_to_test = {
        {"all",    unit_all},
        {"cover",  unit_cover},
        {"errors", unit_except},
        {"api",    unit_api},
        {"c",      unit_c},
    };

    try{
        return string_to_test.at(s);
    }catch(std::out_of_range &){
        return unit_none;
    }
}

bool GridUnitTester::Test(UnitTests test){
    cout << endl << endl;
    cout << "---------------------------------------------------------------------" << endl;
    cout << "       Tasmanian Sparse Grids Module: Unit Tests" << endl;
    cout << "---------------------------------------------------------------------" << endl << endl;

    bool testCover = true;
    bool testExceptions = true;
    bool testAPI = true;
    bool testC = true;

    if ((test == unit_all) || (test == unit_cover)) testCover = testCoverUnimportant();
    if ((test == unit_all) || (test == unit_except)) testExceptions = testAllException();
    if ((test == unit_all) || (test == unit_api)) testAPI = testAPIconsistency();
    if ((test == unit_all) || (test == unit_c)) testC = testCInterface();

    bool pass = testCover && testExceptions && testAPI && testC;
    //bool pass = true;

    cout << endl;
    if (pass){
        cout << "---------------------------------------------------------------------" << endl;
        cout << "           All Unit Tests Completed Successfully" << endl;
        cout << "---------------------------------------------------------------------" << endl << endl;
    }else{
        cout << "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL" << endl;
        cout << "         Some Unit Tests Have Failed" << endl;
        cout << "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL" << endl << endl;
    }
    return pass;
}

bool GridUnitTester::testAllException(){
    bool pass = true;
    bool passAll = true;
    int wfirst = 15, wsecond = 30, wthird = 15;

    // perform std::invalid_argument tests
    auto tests = getInvalidArgumentCalls();
    int test_count = 0;
    for(auto &t : tests)
        try{
            test_count++;
            t(); // run the test
            cout << "Missed arg exception for test " << test_count << " see GridUnitTester::getInvalidArgumentCalls()" << endl;
            pass = false;
            break;
        }catch(std::invalid_argument &){
            //cout << "Got argument error exception on test " << test_count << " with message: " << e.what() << endl;
        }

    if (verbose)
        cout << setw(wfirst) << "Exception" << setw(wsecond) << "std::invalid_argument" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;

    passAll = passAll && pass;
    pass = true;

    // perform std::runtime_error tests
    tests = getRuntimeErrorCalls();
    test_count = 0;
    for(auto &t : tests)
        try{
            test_count++;
            t();
            cout << "Missed runtime exception for test " << test_count << " see GridUnitTester::getRuntimeErrorCalls()" << endl;
            pass = false;
            break;
        }catch(std::runtime_error &){
            //cout << "Got runtime error exception on test " << test_count << " with message: " << e.what() << endl;
        }

    if (verbose)
        cout << setw(wfirst) << "Exception" << setw(wsecond) << "std::runtime_error" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;

    passAll = passAll && pass;

    cout << setw(wfirst+1) << "Exceptions" << setw(wsecond-1) << "" << setw(wthird) << ((passAll) ? "Pass" : "FAIL") << endl;

    return pass;
}

bool GridUnitTester::doesMatch(const std::vector<double> &a, const std::vector<double> &b, double prec) const{
    if (a.size() != b.size()) return false;
    auto ib = b.begin();
    for(auto x : a) if (std::abs(x - *ib++) > prec) return false;
    return true;
}
bool GridUnitTester::doesMatch(const std::vector<double> &a, const double b[], double prec) const{
    auto ib = b;
    for(auto x : a) if (std::abs(x - *ib++) > prec) return false;
    return true;
}
bool GridUnitTester::doesMatch(const std::vector<int> &a, const int b[]) const{
    auto ib = b;
    for(auto x : a) if (x != *ib++) return false;
    return true;
}
bool GridUnitTester::doesMatch(size_t n, double a[], const double b[], double prec) const{
    for(size_t i=0; i<n; i++) if (std::abs(a[i] - b[i]) > prec) return false;
    return true;
}

bool GridUnitTester::testAPIconsistency(){
    bool passAll = true;
    int wfirst = 15, wsecond = 30, wthird = 15;

    // test array and vector consistency between the two versions of the API
    bool pass = true;
    std::vector<double> vpoints;

    TasmanianSparseGrid grid;
    grid.makeGlobalGrid(2, 1, 4, type_iptotal, rule_clenshawcurtis);
    gridLoadEN2(&grid);
    grid.setAnisotropicRefinement(type_iptotal, 10, 0);

    if (verbose) cout << setw(wfirst) << "API variation" << setw(wsecond) << "getPoints()" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;
    passAll = pass && passAll;

    pass = true;
    std::vector<double> vy, x = {0.333, -0.333};
    double *ay = new double[2];

    grid.evaluate(x, vy);
    grid.evaluate(x.data(), ay);
    pass = pass && doesMatch(vy, ay);
    vy.clear();

    grid.integrate(vy);
    grid.integrate(ay);
    pass = pass && doesMatch(vy, ay);
    vy.clear();
    delete[] ay;

    std::vector<double> vf, vx = {0.333, 0.44, -0.1333, 0.2223};
    double *af = new double[grid.getNumPoints() * 2];
    grid.evaluateHierarchicalFunctions(vx.data(), 2, af);
    grid.evaluateHierarchicalFunctions(vx, vf);
    pass = pass && doesMatch(vf, af);
    delete[] af;

    if (verbose) cout << setw(wfirst) << "API variation" << setw(wsecond) << "evaluate/integrate" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;
    passAll = pass && passAll;

    std::vector<double> vtransa = {-2.0, 1.0}, vtransb = {1.0, 2.0};
    double atransa[2], atransb[2];

    grid.setDomainTransform(vtransa, vtransb);
    grid.getDomainTransform(atransa, atransb);
    pass = pass && doesMatch(vtransa, atransa) && doesMatch(vtransb, atransb);

    grid.clearDomainTransform();
    grid.getDomainTransform(vtransa, vtransb);
    if (vtransa.size() + vtransb.size() != 0) pass = false;

    if (verbose) cout << setw(wfirst) << "API variation" << setw(wsecond) << "domain transform" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;
    passAll = pass && passAll;

    int allimits[3] = {1, 2, 3};
    grid.makeGlobalGrid(3, 2, 5, type_iptotal, rule_fejer2, 0, 0.0, 0.0, 0, allimits);
    auto llimits = grid.getLevelLimits();
    pass = pass && doesMatch(llimits, allimits) && (llimits.size() == 3);
    grid.clearLevelLimits();
    llimits = grid.getLevelLimits();
    if (llimits.size() != 0) pass = false;

    if (verbose) cout << setw(wfirst) << "API variation" << setw(wsecond) << "level limits" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;
    passAll = pass && passAll;

    // test integer-to-enumerate and string-to-enumerate conversion
    pass = true;
    std::vector<TypeAcceleration> allacc = {accel_none, accel_cpu_blas, accel_gpu_default, accel_gpu_cublas, accel_gpu_cuda, accel_gpu_magma};
    for(auto acc : allacc){
        if (acc != AccelerationMeta::getIOAccelerationString(AccelerationMeta::getIOAccelerationString(acc))){
            cout << "ERROR: mismatch in string to accel conversion: " << AccelerationMeta::getIOAccelerationString(acc) << endl;
            pass = false;
        }
        if (acc != AccelerationMeta::getIOIntAcceleration(AccelerationMeta::getIOAccelerationInt(acc))){
            cout << "ERROR: mismatch in string to accel conversion: " << AccelerationMeta::getIOIntAcceleration(acc) << endl;
            pass = false;
        }
    }

    cout << setw(wfirst+1) << "API variations" << setw(wsecond-1) << "" << setw(wthird) << ((passAll) ? "Pass" : "FAIL") << endl;
    return passAll;
}

bool GridUnitTester::testCInterface(){
    bool pass = (testInterfaceC() != 0);
    int wfirst = 15, wsecond = 30, wthird = 15;
    cout << setw(wfirst+1) << "C interface" << setw(wsecond-1) << "" << setw(wthird) << ((pass) ? "Pass" : "FAIL") << endl;
    return pass;
}

bool GridUnitTester::testCoverUnimportant(){
    // some code is hard/impractical to test automatically, but untested code shows in coverage reports
    // this function gives coverage to such special cases to avoid confusion in the report

    const char *str = TasmanianSparseGrid::getGitCommitHash();
    const char *str2 = TasmanianSparseGrid::getCmakeCxxFlags();
    str = TasmanianSparseGrid::getCmakeCxxFlags();
    if (str[0] != str2[0]){
        cout << "ERROR: mismatch in strings in testCoverUnimportant()" << endl;
        return false;
    }

    std::vector<TypeOneDRule> rules = {rule_none, rule_clenshawcurtis, rule_clenshawcurtis0, rule_chebyshev, rule_chebyshevodd, rule_gausslegendre, rule_gausslegendreodd, rule_gausspatterson, rule_leja, rule_lejaodd, rule_rleja, rule_rlejadouble2, rule_rlejadouble4, rule_rlejaodd, rule_rlejashifted, rule_rlejashiftedeven, rule_rlejashifteddouble, rule_maxlebesgue, rule_maxlebesgueodd, rule_minlebesgue, rule_minlebesgueodd, rule_mindelta, rule_mindeltaodd, rule_gausschebyshev1, rule_gausschebyshev1odd, rule_gausschebyshev2, rule_gausschebyshev2odd, rule_fejer2, rule_gaussgegenbauer, rule_gaussgegenbauerodd, rule_gaussjacobi, rule_gaussjacobiodd, rule_gausslaguerre, rule_gausslaguerreodd, rule_gausshermite, rule_gausshermiteodd, rule_customtabulated, rule_localp, rule_localp0, rule_semilocalp, rule_localpb, rule_wavelet, rule_fourier};
    for(auto r : rules) str = OneDimensionalMeta::getHumanString(r);

    if (!AccelerationMeta::isAccTypeGPU(accel_gpu_default)){
        cout << "ERROR: mismatch in isAccTypeFullMemoryGPU()" << endl;
        return false;
    }

    RuleWavelet rule(1, 10);
    str = rule.getDescription();
    rule.updateOrder(3);
    str = rule.getDescription();

    return true;
}

std::vector<std::function<void(void)>> GridUnitTester::getInvalidArgumentCalls() const{
    return std::vector<std::function<void(void)>>{
        [](void)->void{
            auto grid = makeGlobalGrid(0, 1, 3, type_level, rule_gausslegendre); // dimension is 0
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, -1, 3, type_level, rule_gausslegendre); // output is -1
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 2, -1, type_level, rule_rleja);  // depth is -1
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 2, 1, type_level, rule_localp);  // rule is localp
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 2, 2, type_level, rule_rleja, {3});  // aw is too short
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 2, 2, type_level, rule_customtabulated);  // custom filename is empty
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 2, 2, type_level, rule_chebyshev, {}, 0.0, 0.0, nullptr, {3});  // level limits is too short
        },
        [](void)->void{
            auto grid = makeSequenceGrid(0, 1, 3, type_level, rule_rleja);  // dimension is 0
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, -1, 3, type_level, rule_minlebesgue);  // output is -1
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 2, -1, type_level, rule_rleja);  // depth is -1
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 3, type_level, rule_localp);  // localp is not a sequence rule
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 2, 2, type_level, rule_rleja, {3});  // aw is too short
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 2, 2, type_level, rule_chebyshev, {}, {3});  // level limits is too short
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(0,  1,  3,  3, rule_localp);  // 0 is not valid dimensions
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, -1,  3,  2, rule_localp);  // -1 is not valid outputs
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2,  1, -1,  2, rule_localp);  // -1 is not valid depth
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2,  1,  3, -2, rule_localp);  // -2 is not a valid order
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2,  1,  3,  2, rule_mindelta);  // mindelta is not a local rule
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2,  1,  3,  1, rule_localp, {3});  // level limits is too short
        },
        [](void)->void{
            auto grid = makeWaveletGrid(0,  1,  3,  1);  // 0 is not a valid dimensions
        },
        [](void)->void{
            auto grid = makeWaveletGrid(2, -1,  3,  1);  // -1 is not a valid outputs
        },
        [](void)->void{
            auto grid = makeWaveletGrid(2,  1, -3,  1);  // -3 is not a valid depth
        },
        [](void)->void{
            auto grid = makeWaveletGrid(2,  1,  3,  2);  // 2 is not a valid order for wavelets
        },
        [](void)->void{
            auto grid = makeWaveletGrid(2,  1,  3,  1, {3});  // level limits is too short
        },
        [](void)->void{
            auto grid = makeFourierGrid(0, 1, 3, type_level);  // dimension is 0
        },
        [](void)->void{
            auto grid = makeFourierGrid(2, -1, 3, type_level);  // output is -1
        },
        [](void)->void{
            auto grid = makeFourierGrid(2, 2, -1, type_level);  // depth is -1
        },
        [](void)->void{
            auto grid = makeFourierGrid(2, 2, 2, type_level, {3});  // aw is too short
        },
        [](void)->void{
            auto grid = makeFourierGrid(2, 2, 2, type_level, {}, {3});  // level limits is too short
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateGlobalGrid(-1, type_level);  // depth is negative
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateGlobalGrid(3, type_level, {3});  // aw is too small
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateGlobalGrid(3, type_level, {}, {3});  // ll is too small
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateSequenceGrid(-1, type_level);  // depth is negative
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateSequenceGrid(3, type_level, {3});  // aw is too small
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateSequenceGrid(3, type_level, {}, {3});  // ll is too small
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.setAnisotropicRefinement(type_iptotal, -1, 0, {1, 2});  // min_growth is negative
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            grid.setAnisotropicRefinement(type_iptotal, 1, 2, {});  // output out of range
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            grid.setAnisotropicRefinement(type_iptotal, 1, 0, {3});  // ll is too small
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 2);  // output out of range
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, 2);  // output out of range
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, 0, {3});  // ll is too small
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(-0.1, 0);  // tolerance is negative
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, refine_classic, 2);  // output out of range
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, refine_classic, 0, {3});  // ll is too small
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(-0.1, refine_classic, 0);  // tolerance is negative
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(-0.1, refine_classic, 0, {3, 2}, {3.0, 3.0});  //scale too small
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            grid.setDomainTransform({1.0}, {3.0, 4.0});  // a is too small
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            grid.setDomainTransform({1.0, 2.0}, {4.0});  // b is too small
        },
        [](void)->void{
            CustomTabulated custom;
            custom.read("phantom.file");
        },
    };
}

std::vector<std::function<void(void)>> GridUnitTester::getRuntimeErrorCalls() const{
    return std::vector<std::function<void(void)>>{
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.updateGlobalGrid(2, type_level);  // grid not initialized
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateGlobalGrid(2, type_level);  // grid not global
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.updateSequenceGrid(2, type_level);  // grid not initialized
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.updateSequenceGrid(2, type_level);  // grid not sequence
        },
        [](void)->void{
            std::vector<double> v;
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.getInterpolationWeights({0.33}, v);  // wrong size of x
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 2, type_level, rule_rleja);
            grid.loadNeededPoints({0.33, 0.22});  // wrong size of loaded data
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 1, type_level, rule_clenshawcurtis);
            grid.loadNeededPoints({0.33, 0.22, 0.22, 0.22, 0.33});
            grid.loadNeededPoints({0.33, 0.22});  // wrong size of loaded data (when overwriting)
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 0, type_level, rule_fejer2);
            double a[2], b[2];
            grid.getDomainTransform(a, b); // cannot call getDomainTransform(array overload) without transform
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setAnisotropicRefinement(type_iptotal, 1, 0, 0);  // grid not made
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setAnisotropicRefinement(type_iptotal, 1, 0, {});  // grid not made
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 0, 3, type_level, rule_rleja);
            grid.setAnisotropicRefinement(type_iptotal,  1, 0, {});  // no outputs
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.setAnisotropicRefinement(type_iptotal,  1, 0, {});  // no loaded values
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            gridLoadEN2(&grid);
            grid.setAnisotropicRefinement(type_iptotal,  1, 0, {});  // rule non-nested
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setAnisotropicRefinement(type_iptotal,  1, 0,{});  // grid is localp
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 1);  // grid not made
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 0, 3, type_level, rule_rleja);
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 0);  // no outputs
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 0);  // no loaded values
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            gridLoadEN2(&grid);
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 0);  // rule non-nested
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            auto w = grid.estimateAnisotropicCoefficients(type_iptotal, 0);  // grid is localp
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setSurplusRefinement(0.01, 0, 0);  // grid not init
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setSurplusRefinement(0.01, 0, {});  // grid not init
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 0, 3, type_level, rule_rleja);
            grid.setSurplusRefinement(0.01, 0, {});  // no outputs
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_rleja);
            grid.setSurplusRefinement(0.01, 0, {});  // no loaded values
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, 0, {});  // rule non-nested
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, 0, {});  // grid is localp
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setSurplusRefinement(0.01, refine_classic, 0, 0);  // grid not init
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setSurplusRefinement(0.01, refine_classic, 0, {});  // grid not init
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 0, 3);
            grid.setSurplusRefinement(0.01, refine_classic, 0);  // no outputs
        },
        [](void)->void{
            auto grid = makeLocalPolynomialGrid(2, 1, 3);
            grid.setSurplusRefinement(0.01, refine_classic, 0);  // no loaded values
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, refine_classic, 0, std::vector<int>());  // rule non-local
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            gridLoadEN2(&grid);
            grid.setSurplusRefinement(0.01, refine_classic, 0, 0);  // rule non-local
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setDomainTransform({}, {});  // grid is not initialized
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setDomainTransform(nullptr, nullptr);  // grid is not initialized
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.setConformalTransformASIN({4, 4});  // grid is not initialized
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            auto transform = grid.getConformalTransformASIN();  // transform not initialized
        },
        [](void)->void{
            auto grid = makeGlobalGrid(2, 1, 3, type_level, rule_chebyshev);
            std::vector<int> pntr, indx;
            std::vector<double> vals;
            std::vector<double> x = {-0.33, 0.33};
            grid.evaluateSparseHierarchicalFunctions(x, pntr, indx, vals);
        },
        [](void)->void{
            TasmanianSparseGrid grid;
            grid.makeGlobalGrid(1, 1, 10, type_level, rule_gausspatterson);  // gauss-patterson rule with very large level
        },
        [](void)->void{
            const char *custom_filename = ExternalTester::findGaussPattersonTable();
            auto grid = makeGlobalGrid(1, 1, 10, type_level, rule_customtabulated, {}, 0.0, 0.0, custom_filename); // custom-tabulated rule with very large level
        },
        [](void)->void{
            CustomTabulated custom;
            custom.read(ExternalTester::findGaussPattersonTable());
            custom.getNumPoints(11); // level too high
        },
        [](void)->void{
            CustomTabulated custom;
            custom.read(ExternalTester::findGaussPattersonTable());
            custom.getIExact(11); // level too high
        },
        [](void)->void{
            CustomTabulated custom;
            custom.read(ExternalTester::findGaussPattersonTable());
            custom.getQExact(11); // level too high
        },
        [](void)->void{
            auto grid = makeSequenceGrid(2, 1, 1, type_level, rule_leja);
            gridLoadEN2(&grid);
            grid.removePointsByHierarchicalCoefficient(0.1, -1, nullptr); // grid is not localp or wavelet
        },
        [](void)->void{
            auto grid = makeEmpty();
            auto integ = grid.integrateHierarchicalFunctions();
        },
    };
}

#endif
