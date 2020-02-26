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

#ifndef __TASMANIAN_TASGRID_FUNCTIONS_CPP
#define __TASMANIAN_TASGRID_FUNCTIONS_CPP

#include "tasgridTestFunctions.hpp"

#include "TasmanianSparseGrid.hpp"

using TasGrid::Maths::pi;

BaseFunction::BaseFunction(){}
BaseFunction::~BaseFunction(){}

OneOneP0::OneOneP0(){} OneOneP0::~OneOneP0(){} int OneOneP0::getNumInputs() const{ return 1; } int OneOneP0::getNumOutputs() const{ return 1; }
const char* OneOneP0::getDescription() const{ return "f(x) = 1"; }
void OneOneP0::eval(const double*, double y[]) const{ y[0] = 1.0; } void OneOneP0::getIntegral(double y[]) const{ y[0] = 2.0; }

OneOneP3::OneOneP3(){} OneOneP3::~OneOneP3(){} int OneOneP3::getNumInputs() const{ return 1; } int OneOneP3::getNumOutputs() const{ return 1; }
const char* OneOneP3::getDescription() const{ return "f(x) = x^3 + 2 x^2 + x + 3"; }
void OneOneP3::eval(const double x[], double y[]) const{ y[0] = x[0]*x[0]*x[0] + 2.0*x[0]*x[0] + x[0] + 3.0; } void OneOneP3::getIntegral(double y[]) const{ y[0] = 22.0/3.0; }

OneOneP4::OneOneP4(){} OneOneP4::~OneOneP4(){} int OneOneP4::getNumInputs() const{ return 1; } int OneOneP4::getNumOutputs() const{ return 1; }
const char* OneOneP4::getDescription() const{ return "f(x) = 0.5 x^4 + x^3 + 2 x^2 + x + 3"; }
void OneOneP4::eval(const double x[], double y[]) const{ y[0] = 0.5*x[0]*x[0]*x[0]*x[0] + x[0]*x[0]*x[0] + 2.0*x[0]*x[0] + x[0] + 3.0; } void OneOneP4::getIntegral(double y[]) const{ y[0] = 226.0/30.0; }

OneOneExpMX::OneOneExpMX(){} OneOneExpMX::~OneOneExpMX(){} int OneOneExpMX::getNumInputs() const{ return 1; } int OneOneExpMX::getNumOutputs() const{ return 1; }
const char* OneOneExpMX::getDescription() const{ return "f(x) = exp(-x^2)"; }
void OneOneExpMX::eval(const double x[], double y[]) const{ y[0] = std::exp(- x[0] * x[0]); } void OneOneExpMX::getIntegral(double y[]) const{ y[0] = 1.493648265624854; }

TwoOneP4::TwoOneP4(){} TwoOneP4::~TwoOneP4(){} int TwoOneP4::getNumInputs() const{ return 2; } int TwoOneP4::getNumOutputs() const{ return 1; }
const char* TwoOneP4::getDescription() const{ return "f(x,y) = x^4 + x^3 y + x^2 y^2 + x^1 y^3 + y^4"; }
void TwoOneP4::eval(const double x[], double y[]) const{ y[0] = x[0]*x[0]*x[0]*x[0] + x[0]*x[0]*x[0]*x[1] + x[0]*x[0]*x[1]*x[1] + x[0]*x[1]*x[1]*x[1] + x[1]*x[1]*x[1]*x[1]; } void TwoOneP4::getIntegral(double y[]) const{ y[0] = 92.0/45.0; }

TwoOneP5::TwoOneP5(){} TwoOneP5::~TwoOneP5(){} int TwoOneP5::getNumInputs() const{ return 2; } int TwoOneP5::getNumOutputs() const{ return 1; }
const char* TwoOneP5::getDescription() const{ return "f(x,y) = x^5 + x^4 y + x^3 y^2 + x^2 y^3 + x y^4 + y^5"; }
void TwoOneP5::eval(const double x[], double y[]) const{ y[0] = x[0]*x[0]*x[0]*x[0]*x[0] + x[0]*x[0]*x[0]*x[0]*x[1] + x[0]*x[0]*x[0]*x[1]*x[1] + x[0]*x[0]*x[1]*x[1]*x[1] + x[0]*x[1]*x[1]*x[1]*x[1] + x[1]*x[1]*x[1]*x[1]*x[1]; } void TwoOneP5::getIntegral(double y[]) const{ y[0] = 0.0; }

TwoOneExpNX2::TwoOneExpNX2(){} TwoOneExpNX2::~TwoOneExpNX2(){} int TwoOneExpNX2::getNumInputs() const{ return 2; } int TwoOneExpNX2::getNumOutputs() const{ return 1; }
const char* TwoOneExpNX2::getDescription() const{ return "f(x,y) = exp(-x^2 - y^2)"; }
void TwoOneExpNX2::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]*x[0] - x[1]*x[1]); } void TwoOneExpNX2::getIntegral(double y[]) const{ y[0] = 2.230985141404134; }

ThreeOneExpNX2::ThreeOneExpNX2(){} ThreeOneExpNX2::~ThreeOneExpNX2(){} int ThreeOneExpNX2::getNumInputs() const{ return 3; } int ThreeOneExpNX2::getNumOutputs() const{ return 1; }
const char* ThreeOneExpNX2::getDescription() const{ return "f(x,y,z) = exp(-x^2 - y^2 - z^2)"; }
void ThreeOneExpNX2::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]*x[0] - x[1]*x[1] - x[2]*x[2]); } void ThreeOneExpNX2::getIntegral(double y[]) const{ y[0] = 3.332307087; }

TwoOneCos::TwoOneCos(){} TwoOneCos::~TwoOneCos(){} int TwoOneCos::getNumInputs() const{ return 2; } int TwoOneCos::getNumOutputs() const{ return 1; }
const char* TwoOneCos::getDescription() const{ return "f(x,y) = cos(-x^2 - y^2 + xy)"; }
void TwoOneCos::eval(const double x[], double y[]) const{ y[0] = std::cos(-x[0]*x[0] - x[1]*x[1] + x[0]*x[1]); } void TwoOneCos::getIntegral(double y[]) const{ y[0] = 2.8137178748032379; }

TwoOneSinSin::TwoOneSinSin(){} TwoOneSinSin::~TwoOneSinSin(){} int TwoOneSinSin::getNumInputs() const{ return 2; } int TwoOneSinSin::getNumOutputs() const{ return 1; }
const char* TwoOneSinSin::getDescription() const{ return "f(x,y) = sin(pi * x) sin(pi * y)"; }
void TwoOneSinSin::eval(const double x[], double y[]) const{ y[0] = std::sin(pi * x[0]) * std::sin(pi * x[1]); } void TwoOneSinSin::getIntegral(double y[]) const{ y[0] = 0.0; }

TwoOneCosCos::TwoOneCosCos(){} TwoOneCosCos::~TwoOneCosCos(){} int TwoOneCosCos::getNumInputs() const{ return 2; } int TwoOneCosCos::getNumOutputs() const{ return 1; }
const char* TwoOneCosCos::getDescription() const{ return "f(x,y) = cos(pi/2 * x) cos(pi/2 * y)"; }
void TwoOneCosCos::eval(const double x[], double y[]) const{ y[0] = std::cos(0.5 * pi * x[0]) * std::cos(0.5 * pi * x[1]); } void TwoOneCosCos::getIntegral(double y[]) const{ y[0] = 16.0 / (pi * pi); }

TwoOneExpSinCos::TwoOneExpSinCos() {} TwoOneExpSinCos::~TwoOneExpSinCos() {} int TwoOneExpSinCos::getNumInputs() const{ return 2; } int TwoOneExpSinCos::getNumOutputs() const{ return 1; }
const char* TwoOneExpSinCos::getDescription() const{ return "f(x,y) = exp(sin(2*pi*x) + cos(2*pi*y)) on [0,1]^2 "; }
void TwoOneExpSinCos::eval(const double x[], double y[]) const{ y[0] = std::exp(std::sin(2*pi*x[0])+std::cos(2*pi*x[1])); } void TwoOneExpSinCos::getIntegral(double y[]) const{ y[0] = 1.6029228068079633 * 4.0; }

TwoOneSinCosAxis::TwoOneSinCosAxis() {} TwoOneSinCosAxis::~TwoOneSinCosAxis() {} int TwoOneSinCosAxis::getNumInputs() const{ return 2; } int TwoOneSinCosAxis::getNumOutputs() const{ return 1; }
const char* TwoOneSinCosAxis::getDescription() const{ return "f(x,y) = 1.0 + sin(pi * (x + y)) * cos(pi * (x - y)) on [-1,1]^2 "; }
void TwoOneSinCosAxis::eval(const double x[], double y[]) const{ y[0] = 1.0 + std::sin(pi*(x[0] + x[1])) * std::cos(pi*(x[0] - x[1])); } void TwoOneSinCosAxis::getIntegral(double y[]) const{ y[0] = 4.0; }

TwoTwoSinCos::TwoTwoSinCos() {} TwoTwoSinCos::~TwoTwoSinCos() {} int TwoTwoSinCos::getNumInputs() const{ return 2; } int TwoTwoSinCos::getNumOutputs() const{ return 2; }
const char* TwoTwoSinCos::getDescription() const{ return "f(x,y) = [sin(2*pi*x)cos(4*pi*y), x^2*cos(2*pi*x)]"; }
void TwoTwoSinCos::eval(const double x[], double y[]) const{ y[0] = std::sin(2*pi*x[0])*std::cos(4*pi*x[1]); y[1] = x[0]*x[0]*cos(2*pi*x[0]); } void TwoTwoSinCos::getIntegral(double y[]) const{ y[0] = 0.0; y[1] = 1.0 / (2.0 * pi * pi); }

TwoOneExpm40::TwoOneExpm40(){} TwoOneExpm40::~TwoOneExpm40(){} int TwoOneExpm40::getNumInputs() const{ return 2; } int TwoOneExpm40::getNumOutputs() const{ return 1; }
const char* TwoOneExpm40::getDescription() const{ return "f(x,y) = 1.0 / (1.0 + exp(-40.0 * (sqrt(x^2 + y^2) - 0.4)))"; }
void TwoOneExpm40::eval(const double x[], double y[]) const{ y[0] = 1.0 / (1.0 + exp(-40.0 * (std::sqrt(x[0]*x[0] + x[1]*x[1]) - 0.4))); } void TwoOneExpm40::getIntegral(double y[]) const{ y[0] = 0.0; }

FiveOneExpSum::FiveOneExpSum(){} FiveOneExpSum::~FiveOneExpSum(){} int FiveOneExpSum::getNumInputs() const{ return 5; } int FiveOneExpSum::getNumOutputs() const{ return 1; }
const char* FiveOneExpSum::getDescription() const{ return "f(y_i) = 1 + exp(-2 - 0.4 * sum(y_i))"; }
void FiveOneExpSum::eval(const double x[], double y[]) const{ y[0] = 1.0 + std::exp(-2.0 -0.4 * (x[0]+x[1]+x[2]+x[3]+x[4])); } void FiveOneExpSum::getIntegral(double y[]) const{ y[0] = 32.0 + std::exp(-2.0) * pow((1.0/0.4) * (exp(0.4) - std::exp(-0.4)), 5.0); }

SixOneExpSum::SixOneExpSum(){} SixOneExpSum::~SixOneExpSum(){} int SixOneExpSum::getNumInputs() const{ return 6; } int SixOneExpSum::getNumOutputs() const{ return 1; }
const char* SixOneExpSum::getDescription() const{ return "f(y_i) = exp(-sum(x_i^2))"; }
void SixOneExpSum::eval(const double x[], double y[]) const{ y[0] = exp(-x[0]*x[0]-x[1]*x[1]-x[2]*x[2]-x[3]*x[3]-x[4]*x[4]-x[5]*x[5]); } void SixOneExpSum::getIntegral(double y[]) const{ y[0] = 1.110427052269093e+01; }

EightOneCosSum::EightOneCosSum(){} EightOneCosSum::~EightOneCosSum(){} int EightOneCosSum::getNumInputs() const{ return 8; } int EightOneCosSum::getNumOutputs() const{ return 1; }
const char* EightOneCosSum::getDescription() const{ return "f(y_i) = cos(-sum(x_i))"; }
void EightOneCosSum::eval(const double x[], double y[]) const{ y[0] = std::cos(x[0]+x[1]+x[2]+x[3]+x[4]+x[5]+x[6]+x[7]); } void EightOneCosSum::getIntegral(double y[]) const{ y[0] = 6.435067827089459e+01; }

ThreeOneUnitBall::ThreeOneUnitBall(){} ThreeOneUnitBall::~ThreeOneUnitBall(){} int ThreeOneUnitBall::getNumInputs() const{ return 3; } int ThreeOneUnitBall::getNumOutputs() const{ return 1; }
const char* ThreeOneUnitBall::getDescription() const{ return "f(y_i) = 1 if |x| < 1, 0 otherwise"; }
void ThreeOneUnitBall::eval(const double x[], double y[]) const{ if ((x[0]*x[0]+x[1]*x[1]+x[2]*x[2]) <= 1.0){ y[0] = 1.0; }else{ y[0] = 0.0; } } void ThreeOneUnitBall::getIntegral(double y[]) const{ y[0] = (4.0/3.0) * pi; }

TwoOneConstGC1::TwoOneConstGC1(){} TwoOneConstGC1::~TwoOneConstGC1(){} int TwoOneConstGC1::getNumInputs() const{ return 2; } int TwoOneConstGC1::getNumOutputs() const{ return 1; }
const char* TwoOneConstGC1::getDescription() const{ return "f(x,y) = exp(x+y), integrated against 1.0 / (sqrt(1 - x*x) * sqrt(1 - y*y))"; }
void TwoOneConstGC1::eval(const double x[], double y[]) const{ y[0] = std::exp(x[0]+x[1]); } void TwoOneConstGC1::getIntegral(double y[]) const{ y[0] = 15.820213988678377; }

TwoOneConstGC2::TwoOneConstGC2(){} TwoOneConstGC2::~TwoOneConstGC2(){} int TwoOneConstGC2::getNumInputs() const{ return 2; } int TwoOneConstGC2::getNumOutputs() const{ return 1; }
const char* TwoOneConstGC2::getDescription() const{ return "f(x,y) = exp(x+y), integrated against (sqrt(1 - x*x) * sqrt(1 - y*y))"; }
void TwoOneConstGC2::eval(const double x[], double y[]) const{ y[0] = std::exp(x[0] + x[1]); } void TwoOneConstGC2::getIntegral(double y[]) const{ y[0] = 3.152399146392550; }

TwoOneConstGG::TwoOneConstGG(){} TwoOneConstGG::~TwoOneConstGG(){} int TwoOneConstGG::getNumInputs() const{ return 2; } int TwoOneConstGG::getNumOutputs() const{ return 1; }
const char* TwoOneConstGG::getDescription() const{ return "f(x,y) = exp(x+y), integrated against (1 - x*x)^0.3 * (1 - y*y)^0.3"; }
void TwoOneConstGG::eval(const double x[], double y[]) const{ y[0] = std::exp(x[0] + x[1]); } void TwoOneConstGG::getIntegral(double y[]) const{ y[0] = 1.955951775017494*1.955951775017494; }

TwoOneConstGJ::TwoOneConstGJ(){} TwoOneConstGJ::~TwoOneConstGJ(){} int TwoOneConstGJ::getNumInputs() const{ return 2; } int TwoOneConstGJ::getNumOutputs() const{ return 1; }
const char* TwoOneConstGJ::getDescription() const{ return "f(x,y) = exp(x+y), integrated against (1 - x)^0.3 * (1 - x)^0.7 * (1 - y)^0.3 * (1 - y)^0.7"; }
void TwoOneConstGJ::eval(const double x[], double y[]) const{ y[0] = std::exp(x[0] + x[1]); } void TwoOneConstGJ::getIntegral(double y[]) const{ y[0] = 2.093562254087821*2.093562254087821; }

TwoOneConstGGL::TwoOneConstGGL(){} TwoOneConstGGL::~TwoOneConstGGL(){} int TwoOneConstGGL::getNumInputs() const{ return 2; } int TwoOneConstGGL::getNumOutputs() const{ return 1; }
const char* TwoOneConstGGL::getDescription() const{ return "f(x,y) = exp(-x-y), integrated against (x)^0.3 * exp(-x) * (y)^0.3 * exp(-y)"; }
void TwoOneConstGGL::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]-x[1]); } void TwoOneConstGGL::getIntegral(double y[]) const{ y[0] = 0.364486361867136*0.364486361867136; }

TwoOneConstGH::TwoOneConstGH(){} TwoOneConstGH::~TwoOneConstGH(){} int TwoOneConstGH::getNumInputs() const{ return 2; } int TwoOneConstGH::getNumOutputs() const{ return 1; }
const char* TwoOneConstGH::getDescription() const{ return "f(x,y) = exp(-x-y), integrated against |x|^0.3 * exp(-x^2) * |y|^0.3 * exp(-y^2)"; }
void TwoOneConstGH::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]-x[1]); } void TwoOneConstGH::getIntegral(double y[]) const{ y[0] = 1.902578389458335*1.902578389458335; }

TwoOneENX2aniso::TwoOneENX2aniso(){} TwoOneENX2aniso::~TwoOneENX2aniso(){} int TwoOneENX2aniso::getNumInputs() const{ return 2; } int TwoOneENX2aniso::getNumOutputs() const{ return 1; }
const char* TwoOneENX2aniso::getDescription() const{ return "f(x,y) = exp(-x^2 -0.1*y^2)"; }
void TwoOneENX2aniso::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]*x[0] -0.1*x[1]*x[1]); } void TwoOneENX2aniso::getIntegral(double y[]) const{ y[0] = 2.890637511323280e+00; }

SixteenOneActive3::SixteenOneActive3(){} SixteenOneActive3::~SixteenOneActive3(){} int SixteenOneActive3::getNumInputs() const{ return 16; } int SixteenOneActive3::getNumOutputs() const{ return 1; }
const char* SixteenOneActive3::getDescription() const{ return "f(x,y) = x[2] * sin(x[3] + x[15])"; }
void SixteenOneActive3::eval(const double x[], double y[]) const{ y[0] = x[2] * std::sin(x[3] + x[15]); } void SixteenOneActive3::getIntegral(double y[]) const{ y[0] = 0.0; }

TwoOneDivisionAnisotropic::TwoOneDivisionAnisotropic(){} TwoOneDivisionAnisotropic::~TwoOneDivisionAnisotropic(){} int TwoOneDivisionAnisotropic::getNumInputs() const{ return 2; } int TwoOneDivisionAnisotropic::getNumOutputs() const{ return 1; }
const char* TwoOneDivisionAnisotropic::getDescription() const{ return "f(x,y) = 1.0 / ((x[0] - 1.1) * (x[0] + 1.1) * (x[1] - 2) * (x[1] + 2))"; }
void TwoOneDivisionAnisotropic::eval(const double x[], double y[]) const{ y[0] = 1.0 / ((x[0] - 1.1) * (x[0] + 1.1) * (x[1] - 2) * (x[1] + 2)); } void TwoOneDivisionAnisotropic::getIntegral(double y[]) const{ y[0] = 1.520340801458519; }

TwoOne1DCurved::TwoOne1DCurved(){} TwoOne1DCurved::~TwoOne1DCurved(){} int TwoOne1DCurved::getNumInputs() const{ return 2; } int TwoOne1DCurved::getNumOutputs() const{ return 1; }
const char* TwoOne1DCurved::getDescription() const{ return "f(x,y) = exp(-x[0]) + exp(x[1])"; }
void TwoOne1DCurved::eval(const double x[], double y[]) const{ y[0] = std::exp(-x[0]) + exp(x[1]); } void TwoOne1DCurved::getIntegral(double y[]) const{ y[0] = 5.524391382167265; }

TwoOneExpShiftedDomain::TwoOneExpShiftedDomain(){} TwoOneExpShiftedDomain::~TwoOneExpShiftedDomain(){} int TwoOneExpShiftedDomain::getNumInputs() const{ return 2; } int TwoOneExpShiftedDomain::getNumOutputs() const{ return 1; }
const char* TwoOneExpShiftedDomain::getDescription() const{ return "f(x,y) = exp(x[0] / 3.0 + x[1] / 5.0)"; }
void TwoOneExpShiftedDomain::eval(const double x[], double y[]) const{ y[0] = std::exp(x[0]/3.0  + x[1]/5.0); } void TwoOneExpShiftedDomain::getIntegral(double y[]) const{ y[0] = 15.0*(std::exp(26.0/15.0) - std::exp(11.0/15.0) - std::exp(7.0/5.0) + std::exp(2.0/5.0)); }

OneOneConformalOne::OneOneConformalOne(){} OneOneConformalOne::~OneOneConformalOne(){} int OneOneConformalOne::getNumInputs() const{ return 1; } int OneOneConformalOne::getNumOutputs() const{ return 1; }
const char* OneOneConformalOne::getDescription() const{ return "f(x) = 1 / (1 + 5x^2)"; }
void OneOneConformalOne::eval(const double x[], double y[]) const{ y[0] = 1.0 / (1.0 + 5.0 * x[0]*x[0]); } void OneOneConformalOne::getIntegral(double y[]) const{ y[0] = 1.028825601981092; }

TwoOneConformalOne::TwoOneConformalOne(){} TwoOneConformalOne::~TwoOneConformalOne(){} int TwoOneConformalOne::getNumInputs() const{ return 2; } int TwoOneConformalOne::getNumOutputs() const{ return 1; }
const char* TwoOneConformalOne::getDescription() const{ return "f(x) = 1 / ((1 + 5x^2)*(1 + 5y^2))"; }
void TwoOneConformalOne::eval(const double x[], double y[]) const{ y[0] = 1.0 / ((1.0 + 5.0*x[0]*x[0]) * (1.0 + 5.0*x[1]*x[1])); } void TwoOneConformalOne::getIntegral(double y[]) const{ y[0] = 1.028825601981092*1.028825601981092; }

Two3KExpSinCos::Two3KExpSinCos(){} Two3KExpSinCos::~Two3KExpSinCos(){} int Two3KExpSinCos::getNumInputs() const{ return 2; } int Two3KExpSinCos::getNumOutputs() const{ return 3072; }
const char* Two3KExpSinCos::getDescription() const{ return "f(x) = exp(x+y), 1+sin(x+y), cos(3*x+y)"; }
void Two3KExpSinCos::eval(const double x[], double y[]) const{
    for(int i=0; i<1025; i++){
        y[i] = std::exp(x[0] + x[1]);
    }
    for(int i=1025; i<2055; i++){
        y[i] = std::sin(x[0] + x[1]) + 1.0;
    }
    for(int i=2055; i<3072; i++){
        y[i] = std::cos(3.0*x[0] + x[1]);
    }
}
void Two3KExpSinCos::getIntegral(double y[]) const{
    for(int i=0; i<1025; i++){
        y[i] = 1.902578389458335*1.902578389458335;
    }
    for(int i=1025; i<2055; i++){
        y[i] = 4.0;
    }
    for(int i=2055; i<3072; i++){
        y[i] = 0.158331189544313;
    }
}

TwoOneC1C2Periodic::TwoOneC1C2Periodic(){} TwoOneC1C2Periodic::~TwoOneC1C2Periodic(){} int TwoOneC1C2Periodic::getNumInputs() const{ return 2; } int TwoOneC1C2Periodic::getNumOutputs() const { return 1; }
const char* TwoOneC1C2Periodic::getDescription() const{ return "f(x,y) = (x^3-x) + (y^4-2y^2)"; }
void TwoOneC1C2Periodic::eval(const double x[], double y[]) const { y[0] = x[0] * (x[0] * x[0] - 1.0) + x[1] * x[1] * (x[1] * x[1] - 2.0); } void TwoOneC1C2Periodic::getIntegral(double y[]) const{ y[0] = -28.0 / 15.0; }


#endif
