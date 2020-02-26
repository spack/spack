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

#ifndef __TASMANIAN_TASDREAM_EXTERNAL_TESTS_CPP
#define __TASMANIAN_TASDREAM_EXTERNAL_TESTS_CPP

#include "tasdreamExternalTests.hpp"

double DreamExternalTester::getChiValue(size_t num_degrees){
    switch(num_degrees){
        case   9: return  21.666;
        case  15: return  30.578;
        case  19: return  36.191;
        case  20: return  37.566;
        case  24: return  42.980;
        case  49: return  74.919;
        case  99: return 134.642;
        case 124: return 163.546;
        default:
            throw std::runtime_error("ERROR: Unknown degrees of freedom for the Chi-squared test.");
    }
}

bool DreamExternalTester::testFit(const std::vector<int> &cell_count_a, const std::vector<int> &cell_count_b){
    double suma = (double) std::accumulate(cell_count_a.begin(), cell_count_a.end(), 0);
    double sumb = (double) std::accumulate(cell_count_b.begin(), cell_count_b.end(), 0);

    double scale = std::sqrt(sumb / suma);

    double test_value = 0.0;

    auto ia = cell_count_a.begin(), ib = cell_count_b.begin();
    while(ia != cell_count_a.end()){
        double diff = ((double) *ia) * scale - ((double) *ib) / scale;
        double sum = (double) (*ia++ + *ib++);
        if (sum > 0.0) test_value += diff * diff / sum;
    }

    bool pass = (test_value < getChiValue(cell_count_a.size() - 1));
    if (!pass || showvalues){
        if (!pass) cout << "Chi-Squared test FAILED" << endl;
        cout << "Totals: " << suma << "  " << sumb << endl;
        cout << "Chi-Squared test value = " << test_value << " num cells: " << cell_count_a.size() << endl;
        cout << "Critical Chi-Squared value = " << getChiValue(cell_count_a.size() - 1) << endl;
    }

    return pass;
}

void DreamExternalTester::binHypercubeSamples(const std::vector<double> &lower, const std::vector<double> &upper, int num_bins1D, const std::vector<double> &data, std::vector<int> &bin_count){
    size_t num_dimensions = lower.size();
    if (upper.size() != num_dimensions) throw std::runtime_error("ERROR: upper and lower must have the same size in binHypercubeSamples() DREAM testing");

    std::vector<double> dx(num_dimensions);
    auto il = lower.begin(), iu = upper.begin();
    for(auto &d : dx) d = (*iu++ - *il++) / ((double) num_bins1D);

    size_t num_bins = 1;
    for(size_t i=0; i<num_dimensions; i++) num_bins *= num_bins1D;
    bin_count = std::vector<int>(num_bins, 0);

    auto id = data.begin();
    while(id != data.end()){
        std::vector<size_t> binid(num_dimensions);
        il = lower.begin();
        iu = dx.begin();
        for(auto &i : binid){
            i = (size_t) ((*id++ - *il++) / *iu++);
            if (i >= (size_t) num_bins1D) i = num_bins1D-1;
        }
        size_t bin_index = 0;
        for(auto i : binid) bin_index = num_dimensions * bin_index + i;
        bin_count[bin_index]++;
    }
}

bool DreamExternalTester::compareSamples(const std::vector<double> &lower, const std::vector<double> &upper, int num_bins1D,
                                         const std::vector<double> &data1, const std::vector<double> &data2){
    std::vector<int> count1, count2;
    binHypercubeSamples(lower, upper, num_bins1D, data1, count1);
    binHypercubeSamples(lower, upper, num_bins1D, data2, count2);
    return testFit(count1, count2);
}

bool DreamExternalTester::testGaussian3D(){
    bool passAll = true;
    int num_dimensions = 3;
    int num_samples = 1000, num_chains = 20;
    int num_iterations = num_samples / num_chains + 2;
    int num_burnup = 20 * num_iterations;

    std::minstd_rand park_miller(42);
    if (usetimeseed) park_miller.seed(getRandomRandomSeed());
    std::uniform_real_distribution<double> unif(0.0, 1.0);
    auto get_rand = [&]()->double{ return unif(park_miller); };

    // compute reference samples, mean 2.0, std 3.0
    std::vector<double> means(num_dimensions, 2.0), deviations(num_dimensions, 3.0);
    std::vector<double> tresult = genGaussianSamples(means, deviations, num_samples, get_rand);

    // Use DREAM with zero-weight (i.e., standard Metropolis-Hastings)
    TasmanianDREAM state(num_chains, num_dimensions);
    // initialize with correct mean 2.0, std 3.0
    std::vector<double> initial_state = genGaussianSamples(means, deviations, num_chains, get_rand);
    state.setState(initial_state);

    SampleDREAM(num_burnup, num_iterations,
        [&](const std::vector<double> &candidates, std::vector<double> &values){
            // 3D Gaussian PDF with standard deviation of 3.0
            auto ix = candidates.begin();
            for(auto &v : values)
                v = getDensity<dist_gaussian>(*ix++, 2.0, 9.0) * getDensity<dist_gaussian>(*ix++, 2.0, 9.0) * getDensity<dist_gaussian>(*ix++, 2.0, 9.0);
        },
        [&](const std::vector<double>&)->bool{ return true; }, // unbounded domain
        state,
        [&](std::vector<double> &x){
            applyGaussianUpdate(x, 3.0, [&]()->double{ return unif(park_miller); });
        },
        const_percent<0>, // independent chains, no differential proposal
        get_rand
    );

    std::vector<double> upper(num_dimensions, 11.0), lower(num_dimensions, -7.0); // compute over a box of 3 standard deviations

    bool pass = compareSamples(lower, upper, 5, tresult, state.getHistory());
    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Gaussian 3D", "with independent chains");

    state = TasmanianDREAM(num_chains, num_dimensions); // reinitialize
    state.setState(initial_state);

    SampleDREAM(num_burnup, 2*num_iterations,
        [&](const std::vector<double> &candidates, std::vector<double> &values){
            // 3D Gaussian PDF with standard deviation of 3.0
            auto ix = candidates.begin();
            for(auto &v : values)
                v = getDensity<dist_gaussian>(*ix++, 2.0, 9.0) * getDensity<dist_gaussian>(*ix++, 2.0, 9.0) * getDensity<dist_gaussian>(*ix++, 2.0, 9.0);
        },
        hypercube(lower, upper), // large domain
        state,
        dist_uniform, 0.2, // uniform proposal
        const_percent<50>, // differential proposal is weighted by 50%
        get_rand
    );

    pass = compareSamples(lower, upper, 5, tresult, state.getHistory()) && (state.getAcceptanceRate() > 0.5);
    passAll = passAll && pass;

    if (verbose || !pass) reportPassFail(pass, "Gaussian 3D", "with correlated chains");

    // test anisotropic Gaussian likelihood
    // compute reference samples, compute initial set from the true solution, reinitialize the state
    tresult       = genGaussianSamples({1.5, 2.0, 2.5}, {0.5, 1.0, 2.0}, num_samples, get_rand);
    initial_state = genGaussianSamples({1.5, 2.0, 2.5}, {0.5, 1.0, 2.0}, num_chains, get_rand);
    state = TasmanianDREAM(num_chains, num_dimensions); // reinitialize
    state.setState(initial_state);
    LikelihoodGaussAnisotropic likely({0.25, 1.0, 4.0}, {1.5, 2.0, 2.5}, 1);
    if (likely.getNumOutputs() != 3) throw std::runtime_error("LikelihoodGaussAnisotropic has wrong num outputs");

    SampleDREAM(num_burnup, num_iterations,
        posterior(
            [&](const std::vector<double> &candidates, std::vector<double> &values){
                values = candidates; // the model is identity
            },
            likely, uniform_prior),
        hypercube(lower, upper), // large domain
        state,
        dist_uniform, 0.2,
        const_percent<50>, // differential proposal is weighted by 50%
        get_rand
    );

    pass = compareSamples(lower, upper, 5, tresult, state.getHistory()) && (state.getAcceptanceRate() > 0.5);

    std::vector<double> mean, variance;
    state.getHistoryMeanVariance(mean, variance);
    std::vector<double> tmean = {1.5, 2.0, 2.5}, tvar = {0.25, 1.0, 4.0};
    for(int i=0; i<3; i++) {
        if (std::abs(mean[i] - tmean[i]) / tmean[i] > 0.3){
            cout << "error in mean exceeded: " << std::abs(mean[i] - tmean[i]) / tmean[i] << endl;
            pass = false;
        }
        if (std::abs(variance[i] - tvar[i]) / tvar[i] > 0.6){
            cout << "error in variance exceeded: " << std::abs(variance[i] - tvar[i]) / tvar[i] << endl;
            pass = false;
        }
    }
    state = TasmanianDREAM(); // reset to empty test
    if (state.getNumDimensions() != 0) throw std::runtime_error("TasmanianDREAM has wrong num dimensions");

    passAll = passAll && pass;

    if (verbose || !pass) reportPassFail(pass, "Gaussian 3D", "with anisotropic likelihood");

    reportPassFail(passAll, "Gaussian 3D", "DREAM vs Box-Muller");

    return passAll;
}

bool DreamExternalTester::testGaussian2D(){
    bool passAll = true;
    int num_dimensions = 2;
    int num_samples = 1000, num_chains = 20;
    int num_iterations = num_samples / num_chains + 2;
    int num_burnup = 20 * num_iterations;

    std::minstd_rand park_miller(42);
    if (usetimeseed) park_miller.seed(getRandomRandomSeed());
    std::uniform_real_distribution<double> unif(0.0, 1.0);
    auto get_rand = [&]()->double{ return unif(park_miller); };

    // compute reference samples, mean 0.3, std 0.15 (3 deviations fit in [-1, 1]^2)
    std::vector<double> tresult(num_dimensions * num_samples, 0.3);
    applyGaussianUpdate(tresult, 0.15, get_rand);

    // approximate the pdf in log-form, log-form of the Gaussian pdf is quadratic, the grid gives exact match
    TasGrid::TasmanianSparseGrid grid;
    grid.makeSequenceGrid(2, 1, 2, TasGrid::type_iptotal, TasGrid::rule_rleja); // interpolates exactly all quadratic polynomials
    std::vector<double> grid_points, values;
    grid.getNeededPoints(grid_points);
    values.resize(grid_points.size() / 2);
    auto ip = grid_points.begin();
    for(auto &v : values)
        v = getDensity<dist_gaussian, logform>(*ip++, 0.3, 0.0225) + getDensity<dist_gaussian, logform>(*ip++, 0.3, 0.0225);
    grid.loadNeededPoints(values);

    // initialize the DREAM state
    TasmanianDREAM state(num_chains, num_dimensions);
    std::vector<double> initial_set(num_chains * num_dimensions, 0.0); // initialize with uniform samples
    applyUniformUpdate(initial_set, 1.0, get_rand);
    state.setState(initial_set);

    SampleDREAM<logform>(num_burnup, num_iterations,
        posterior<logform>(grid, uniform_prior),
        grid.getDomainInside(),
        state,
        dist_gaussian, 0.1,
        const_percent<98>, // correlated chains
        get_rand
    );

    std::vector<double> upper(num_dimensions, 1.0), lower(num_dimensions, -1.0); // compute over a box of over 3 standard deviations
    bool pass = compareSamples(lower, upper, 10, tresult, state.getHistory());

    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Gaussian 2D", "with inferred domain");


    // ------------------------------------------------------------ //
    // next test uses a sub-domain of the first quadrant, the standard deviation is smaller
    std::fill(tresult.begin(), tresult.end(), 0.3);
    applyGaussianUpdate(tresult, 0.1, get_rand);

    // approximate the pdf in regular form, true approximation
    grid.makeSequenceGrid(2, 1, 24, TasGrid::type_iptotal, TasGrid::rule_rleja); // interpolates exactly all quadratic polynomials
    grid.getNeededPoints(grid_points);
    values.resize(grid_points.size() / 2);
    ip = grid_points.begin();
    for(auto &v : values) // using tighter variance of 0.01
        v = getDensity<dist_gaussian>(*ip++, 0.3, 0.01) * getDensity<dist_gaussian>(*ip++, 0.3, 0.01);
    grid.loadNeededPoints(values);

    // re-initialize the DREAM state
    state = TasmanianDREAM(num_chains, num_dimensions);
    initial_set = std::vector<double>(tresult.begin(), tresult.begin() + num_chains * num_dimensions);
    state.setState(initial_set);

    lower = std::vector<double>(num_dimensions, 0.0); // consider only the first quadrant
    upper = std::vector<double>(num_dimensions, 1.0);

    SampleDREAM<regform>(num_burnup, num_iterations,
        posterior<regform>(grid, uniform_prior),
        hypercube(lower, upper),
        state,
        dist_uniform, 0.1,
        const_percent<98>, // correlated chains
        [&]()->double{ return unif(park_miller); }
    );

    // check if any of the samples fall outside of the domain
    pass = compareSamples(lower, upper, 10, tresult, state.getHistory()) &&
           std::none_of(state.getHistory().begin(), state.getHistory().end(), [&](double x)->bool{ return ((x < 0.0) || (x>1.0)); });

    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Gaussian 2D", "with custom domain");


    // ------------------------------------------------------------ //
    // next test uses the same sub-domain of the first quadrant, but the grid and prior each define different dimensions

    // approximate the pdf in regular form, true approximation
    grid.makeSequenceGrid(2, 1, 24, TasGrid::type_iptotal, TasGrid::rule_rleja); // interpolates exactly all quadratic polynomials
    grid.getNeededPoints(grid_points);
    values.resize(grid_points.size() / 2);
    ip = grid_points.begin();
    for(auto &v : values){ // using tighter variance of 0.01
        v = getDensity<dist_gaussian>(*ip++, 0.3, 0.01);
        ip++; // skip the second dimension in the likelihood
    }
    grid.loadNeededPoints(values);

    // re-initialize the DREAM state
    state.clearHistory();
    initial_set = std::vector<double>(tresult.begin(), tresult.begin() + num_chains * num_dimensions);
    state.setState(initial_set);

    SampleDREAM<regform>(num_burnup, num_iterations,
        posterior<regform>(grid,
                           [&](TypeSamplingForm, const std::vector<double> &candidates, std::vector<double> &vals)->void{
                               auto ic = candidates.begin();
                               for(auto &v : vals){ // using tighter variance of 0.01
                                   ic++; // skip the first dimension in the likelihood
                                   v = getDensity<dist_gaussian>(*ic++, 0.3, 0.01);
                               }
                           }),
        hypercube(lower, upper),
        state,
        dist_uniform, 0.1,
        const_percent<98>, // correlated chains
        get_rand
    );

    // check if any of the samples fall outside of the domain and if the size of the history is correct
    pass = compareSamples(lower, upper, 10, tresult, state.getHistory()) &&
           std::none_of(state.getHistory().begin(), state.getHistory().end(), [&](double x)->bool{ return ((x < 0.0) || (x>1.0)); }) &&
           (state.getNumHistory() == (size_t)(num_iterations * num_chains));

    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Gaussian 2D", "with custom prior");

    reportPassFail(passAll, "Gaussian 2D", "DREAM-Grid vs Box-Muller");

    return passAll;
}

bool DreamExternalTester::testKnownDistributions(){
    // Test Gaussian distribution

    bool pass1 = testGaussian3D();
    bool pass2 = testGaussian2D();

    return pass1 && pass2;
}

bool DreamExternalTester::testCustomModel(){
    bool passAll = true;
    int num_dimensions = 3;
    int num_samples = 1000, num_chains = 40;
    int num_iterations = num_samples / num_chains + 2;
    int num_burnup = 20 * num_iterations;

    std::minstd_rand park_miller(42);
    if (usetimeseed) park_miller.seed(getRandomRandomSeed());
    std::uniform_real_distribution<double> unif(0.0, 1.0);
    auto get_rand = [&]()->double{ return unif(park_miller); };

    // compute reference samples, means 1.5, 2.0 and 2.5, variance 4.0, 9.0, 4.0
    std::vector<double> tresult = genGaussianSamples({1.5, 2.0, 2.5}, {2.0, 3.0, 2.0}, num_samples, get_rand);

    // Use DREAM with custom model of identity (all information comes form the prior and likelihood)
    TasmanianDREAM state(num_chains, num_dimensions);
    std::vector<double> initial_state(num_chains * num_dimensions, 2.0); // initialize with random samples
    applyGaussianUpdate(initial_state, 3.0, [&]()->double{ return unif(park_miller); });
    state.setState(initial_state);

    LikelihoodGaussIsotropic likely(4.0, {1.5, 2.5});
    if (likely.getNumOutputs() != 2) throw std::runtime_error("LikelihoodGaussAnisotropic has wrong num outputs");
    SampleDREAM(num_burnup, num_iterations,
                    posterior(
                    [&](const std::vector<double> &candidates, std::vector<double> &values)->void{ // model
                        size_t num_candidates = candidates.size() / 3;
                        auto ic = candidates.begin();
                        values.resize(2 * num_candidates);
                        auto iv = values.begin();
                        while(iv != values.end()){ // takes the first and last parameters
                            *iv++ = *ic++;
                            ic++;
                            *iv++ = *ic++;
                        }
                    },
                    likely,
                    [&](TypeSamplingForm, const std::vector<double> &candidates, std::vector<double> &values)->void{ // prior
                        auto ic = candidates.begin() + 1; // uses the second input entries only
                        for(auto &v : values){
                            v = getDensity<dist_gaussian>(*ic, 2.0, 9.0);
                            std::advance(ic, num_dimensions);
                        }
                    }),
                    [&](const std::vector<double>&)->bool{ return true; }, // unbounded domain
                    state,
                    [&](std::vector<double> &x){
                        applyGaussianUpdate(x, 0.5, [&]()->double{ return unif(park_miller); });
                    },
                    const_percent<65>,
                    get_rand
                );

    std::vector<double> upper(num_dimensions, 11.0), lower(num_dimensions, -7.0); // compute over a box of more than 3 standard deviations

    bool pass = compareSamples(lower, upper, 5, tresult, state.getHistory());
    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Inference 3D", "with custom model");

    state = TasmanianDREAM(num_chains, num_dimensions); // reinitialize
    state.setState(genUniformSamples({0.0, 0.0, 0.0}, {1.0, 1.0, 1.0}, num_chains, get_rand));

    lower = std::vector<double>(num_dimensions, 0.0);
    upper = std::vector<double>(num_dimensions, 1.0);

    likely = LikelihoodGaussIsotropic(0.01, {0.0, 0.0});

    SampleDREAM<logform>(num_burnup, num_iterations,
                         posterior<logform>(
                         [&](const std::vector<double> &candidates, std::vector<double> &values)->void{ // model
                             size_t num_candidates = candidates.size() / 3;
                             values.resize(2 * num_candidates);
                             auto ic = candidates.begin();
                             auto iv = values.begin();
                             while(iv != values.end()){ // takes the first and last parameters
                                 *iv++ = 1.0 - std::sin(DreamMaths::pi * *ic++);
                                 ic++;
                                 *iv++ = 1.0 - std::sin(DreamMaths::pi * *ic++);
                             }
                         },
                         likely, uniform_prior),
                         hypercube(lower, upper),
                         state,
                         dist_gaussian, 0.01,
                         const_percent<50>,
                         get_rand
                         );

    std::vector<double> mode;
    state.getApproximateMode(mode);
    //cout << mode[0] << "  " << mode[1] << "  " << mode[2] << "  acceptance = " << state.getAcceptanceRate() << endl;
    pass = ((mode[0] > 0.45) && (mode[0] < 0.55) && (mode[2] > 0.45) && (mode[2] < 0.55) && (state.getAcceptanceRate() > 0.5));
    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Inference 3D", "optimization objective");

    reportPassFail(pass, "Inference 3D", "DREAM Bayesian inference");

    return passAll;
}

bool DreamExternalTester::testGridModel(){
    bool passAll = true;
    int num_dimensions = 2, num_outputs = 64;
    int num_samples = 1000, num_chains = 40;
    int num_iterations = num_samples / num_chains + 2;
    int num_burnup = 20 * num_iterations;

    std::minstd_rand park_miller(42);
    if (usetimeseed) park_miller.seed(getRandomRandomSeed());
    std::uniform_real_distribution<double> unif(0.0, 1.0);
    auto get_rand = [&]()->double{ return unif(park_miller); };

    // Construct sparse grid approximation to the SinSin model
    std::vector<double> lower = {0.0, 2.0}, upper = {4.0, 6.0};
    TasGrid::TasmanianSparseGrid grid;
    grid.makeLocalPolynomialGrid(num_dimensions, num_outputs, 8, 2); // using quadratic basis of level 4
    grid.setDomainTransform(lower, upper); // magnitude is in range (0, 4), frequency in range (2.0, 6.0)
    std::vector<double> points, values(num_outputs * grid.getNumPoints());
    grid.getNeededPoints(points);

    auto ip = points.begin(), iv = values.begin();
    while(ip != points.end()){
        getSinSinModel(*ip, *(ip+1), 1.0 / ((double) num_outputs), num_outputs, &*iv);
        std::advance(ip, num_dimensions);
        std::advance(iv, num_outputs);
    }
    grid.loadNeededPoints(values); // surrogate constructed

    // initialize the state
    TasmanianDREAM state(num_chains, grid);
    state.setState(genUniformSamples(lower, upper, num_chains, get_rand));

    // initialize the likelihood
    std::vector<double> data(num_outputs);
    getSinSinModel(2.0, 5.0, 1.0 / ((double) num_outputs), num_outputs, data.data()); // true magnitude 2.0, frequency 5.0
    LikelihoodGaussIsotropic likely(0.01, data);

    // sample using uniform prior
    SampleDREAM<logform>(num_burnup, num_chains,
                         posterior<logform>(grid, likely, uniform_prior),
                         grid.getDomainInside(),
                         state,
                         dist_gaussian, 0.1, const_percent<50>, get_rand);

    //printMode(state, "mode");
    std::vector<double> mode;
    state.getApproximateMode(mode);
    bool pass = ((mode[0] > 1.0) && (mode[0] < 3.0) && (mode[1] > 4.5) && (mode[1] < 5.5));
    passAll = passAll && pass;
    if (verbose || !pass) reportPassFail(pass, "Inference 2D", "grid frequency model");

    reportPassFail(pass, "Inference 2D", "DREAM Bayesian grid model");

    return passAll;
}

bool DreamExternalTester::testPosteriorDistributions(){
    // Tests using posteriors constructed from model and prior distributions

    bool pass1 = testCustomModel();
    bool pass2 = testGridModel();

    return pass1 && pass2;
}

bool DreamExternalTester::performTests(TypeDREAMTest test){
    cout << endl << endl;
    cout << "---------------------------------------------------------------------" << endl;
    cout << "           Tasmanian DREAM Module: Functionality Test" << endl;
    cout << "---------------------------------------------------------------------" << endl << endl;

    bool pass = true;

    std::vector<int> results(10, 1); // results for all possible tests

    if ((test == test_all) || (test == test_analytic))  results[0] = (testKnownDistributions()) ? 1 : 0;
    if ((test == test_all) || (test == test_posterior)) results[1] = (testPosteriorDistributions()) ? 1 : 0;

    pass = std::all_of(results.begin(), results.end(), [&](int i)->bool{ return (i == 1); });

    cout << endl;
    if (pass){
        cout << "---------------------------------------------------------------------" << endl;
        cout << "           All Tests Completed Successfully" << endl;
        cout << "---------------------------------------------------------------------" << endl << endl;
    }else{
        cout << "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL" << endl;
        cout << "         Some Tests Have Failed" << endl;
        cout << "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL" << endl << endl;
    }
    return pass;
}

void testDebug(){
    cout << "Debug Test" << endl;
    cout << "Put here testing code and call this with ./dreamtest debug" << endl;
}

#endif
