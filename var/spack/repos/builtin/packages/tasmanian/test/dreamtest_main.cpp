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

#include "tasgridCLICommon.hpp"

#include "tasdreamExternalTests.hpp"

using namespace std;

void printHelp();

int main(int argc, const char ** argv){

    //cout << " Phruuuuphrrr " << endl; // this is the sound that the Tasmanian devil makes

    std::deque<std::string> args = stringArgs(argc, argv);
    if (!args.empty() && hasHelp(args.front())){
        printHelp();
        return 0;
    }

    bool debug = false;
    TypeDREAMTest test = test_all;

    DreamExternalTester tester;

    while(!args.empty()){
        if (hasInfo(args.front())){
            tester.showVerbose();
            if ((args.front() == "verbose") || (args.front() == "-verbose"))
                tester.showStatsValues();
        }else if (hasRandom(args.front())) tester.useRandomRandomSeed();
        else if (args.front() == "debug") debug = true;
        else if (args.front() == "analytic") test = test_analytic;
        else if (args.front() == "posterior") test = test_posterior;
        else if (args.front() == "all") test = test_all;
        else{
            cerr << "ERROR: Unknown option '" << args.front() << "'" << endl;
            cerr << "   to see list of available options use: ./dreamtest --help" << endl;
            return 1;
        }
        args.pop_front();
    }

    if (debug){
        testDebug();
        return 0;
    }

    return (tester.performTests(test)) ? 0 : 1;
}

void printHelp(){
    cout << endl;
    cout << "Usage: dreamtest <command1> <command2> ...\n\n";
    cout << "Commands\tAction\n";
    cout << "all\t\tRun all tests (default if no commands are given)\n";
    cout << "analytic\tRun the tests associated with analytic probability distributions\n";
    cout << "posterior\tRun the tests associated with Bayesian inference\n";
    cout << "-v\t\tShow verbose test information\n";
    cout << "verbose\t\tIn addition to -v also shows critical test values\n";
    cout << "random\t\tDo not use the hard-coded random seed, use the time as random seed\n";
    cout << "debug\t\tRun the code implemented in tasdreamExternalTests.cpp function testDebug()\n";
    cout << endl;
}
