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

#include "tasgridExternalTests.hpp"
#include "tasgridUnitTests.hpp"

int main(int argc, const char ** argv){

    //cout << " Phruuuuphrrr " << endl; // this is the sound that the Tasmanian devil makes

    std::deque<std::string> args = stringArgs(argc, argv);

    // testing
    bool debug = false;
    bool debugII = false;
    bool verbose = false;
    bool seed_reset = false;

    TestList test = test_all;
    UnitTests utest = unit_none;

    int gpuid = -1;
    while (!args.empty()){
        if (args.front() == "debug") debug = true;
        if (args.front() == "db") debugII = true;
        if (hasInfo(args.front())) verbose = true;
        if (hasRandom(args.front())) seed_reset = true;
        TestList test_maybe = ExternalTester::hasTest(args.front());
        if (test_maybe != test_none) test = test_maybe;
        UnitTests utest_maybe = GridUnitTester::hasTest(args.front());
        if (utest_maybe != unit_none) utest = utest_maybe;
        if ((args.front() == "-gpuid") || (args.front() == "-gpu")){
            args.pop_front();
            if (args.empty()){
                cerr << "ERROR: -gpuid required a valid number!" << endl;
                return 1;
            }
            gpuid = std::stoi(args.front());
            if ((gpuid < -1) || (gpuid >= TasmanianSparseGrid::getNumGPUs())){
                cerr << "ERROR: -gpuid " << gpuid << " is not a valid gpuid!" << endl;
                cerr << "      see ./tasgrid -v for a list of detected GPUs." << endl;
                return 1;
            }
        }
        args.pop_front();
    }

    ExternalTester tester(1000);
    GridUnitTester utester;
    tester.setGPUID(gpuid);
    bool pass = true;
    if (debug){
        tester.debugTest();
    }else if (debugII){
        tester.debugTestII();
    }else{
        if (verbose) tester.setVerbose(true);
        if (verbose) utester.setVerbose(true);

        if (seed_reset) tester.resetRandomSeed();

        if (utest == unit_none){
            if (test == test_all) pass = pass && utester.Test(unit_all);
            pass = pass && tester.Test(test);
        }else{
            pass = pass && utester.Test(utest);
        }
    }
    return (pass) ? 0 : 1;
}
