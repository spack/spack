# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCritic(PerlPackage):
    """Critique Perl source code for best-practices."""  # AUTO-CPAN2Spack

    homepage = "http://perlcritic.com"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Perl-Critic-1.140.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.140", sha256="bfeef0aa36f0941682a607212593db530b2c8a5499f6dc7d41f7e61a8ebdfddb")
    version("1.139_01", sha256="6fcbf8ab7e9579e3985fc87c92e3ec57eafdc7c609d3e39ed7331675335b1703")

    depends_on("perl-module-build", type="build")

    provides("perl-perl-critic-annotation")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-command")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-config")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-document")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-aggregateconfiguration")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration-generic")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration-nonexistentpolicy")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration-option")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration-option-global")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-exception-configuration-option-global-extraparameter"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-exception-configuration-option-global-parametervalue"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-configuration-option-policy")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-exception-configuration-option-policy-extraparameter"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-exception-configuration-option-policy-parametervalue"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-fatal")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-fatal-generic")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-fatal-internal")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-fatal-policydefinition")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-io")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-exception-parse")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-optionsprocessor")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitbooleangrep")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitcomplexmappings")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitlvaluesubstr")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-builtinfunctions-prohibitreversesortblock"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitshiftref")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitsleepviaselect")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitstringyeval")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitstringysplit")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibituniversalcan")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibituniversalisa")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibituselesstopic")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitvoidgrep")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-prohibitvoidmap")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-requireblockgrep")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-requireblockmap")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-requireglobfunction")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-builtinfunctions-requiresimplesortblock")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-classhierarchies-prohibitautoloading")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-classhierarchies-prohibitexplicitisa")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-classhierarchies-prohibitoneargbless")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibithardtabs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibitparenswithbuiltins")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibitquotedwordlists")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibittrailingwhitespace")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-requireconsistentnewlines")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-requiretidycode")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-requiretrailingcommas")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-controlstructures-prohibitcstyleforloops")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-prohibitcascadingifelse"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-controlstructures-prohibitdeepnests")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-prohibitlabelswithspecialblocknames"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-prohibitmutatinglistfunctions"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-"
        "prohibitnegativeexpressionsinunlessanduntilconditions"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-prohibitpostfixcontrols"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-controlstructures-prohibitunlessblocks")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-controlstructures-prohibitunreachablecode"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-controlstructures-prohibituntilblocks")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-controlstructures-prohibityadaoperator")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-podspelling")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-documentation-requirepackagematchespodname"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirepodatend")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirepodsections")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-errorhandling-requirecarping")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-errorhandling-requirecheckingreturnvalueofeval"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitbacktickoperators")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitbarewordfilehandles")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitexplicitstdin")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitinteractivetest")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitjoinedreadline")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitoneargselect")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibitreadlineinforloop")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-prohibittwoargopen")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-inputoutput-requirebracedfilehandlewithprint"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-requirebriefopen")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-requirecheckedclose")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-requirecheckedopen")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-requirecheckedsyscalls")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-inputoutput-requireencodingwithutf8layer")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-prohibitformats")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-prohibitties")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-prohibitunrestrictednocritic")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-prohibituselessnocritic")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitautomaticexportation")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitconditionalusestatements")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitevilmodules")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitexcessmaincomplexity")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitmultiplepackages")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requirebarewordincludes")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requireendwithone")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requireexplicitpackage")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requirefilenamematchespackage")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requirenomatchvarswithuseenglish")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-requireversionvar")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-namingconventions-capitalization")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-namingconventions-prohibitambiguousnames")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-objects-prohibitindirectsyntax")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-references-prohibitdoublesigils")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitcapturewithouttest"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitcomplexregexes"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitenumeratedclasses"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitescapedmetacharacters"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitfixedstringmatches"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitsinglecharalternation"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-regularexpressions-prohibitunusedcapture")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-prohibitunusualdelimiters"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-regularexpressions-prohibituselesstopic")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-requirebracesformultiline"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-requiredotmatchanything"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-requireextendedformatting"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-regularexpressions-requirelineboundarymatching"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitampersandsigils")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitbuiltinhomonyms")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitexcesscomplexity")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitexplicitreturnundef")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitmanyargs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitnestedsubs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitreturnsort")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-prohibitsubroutineprototypes")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-subroutines-prohibitunusedprivatesubroutines"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-protectprivatesubs")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-requireargunpacking")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-subroutines-requirefinalreturn")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-testinganddebugging-prohibitnostrict")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-testinganddebugging-prohibitnowarnings")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-testinganddebugging-prohibitprolongedstrictureoverride"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-testinganddebugging-requiretestlabels")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-testinganddebugging-requireusestrict")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-testinganddebugging-requireusewarnings")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitcommaseparatedstatements"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitcomplexversion"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitconstantpragma"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitemptyquotes")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitescapedcharacters"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitimplicitnewlines"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitinterpolationofliterals"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitleadingzeros"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitlongchainsofmethodcalls"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitmagicnumbers"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitmismatchedoperators"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitmixedbooleanoperators"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitnoisyquotes")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitquotesasquotelikeoperatordelimiters"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitspecialliteralheredocterminator"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-prohibitversionstrings"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-requireconstantversion"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-requireinterpolationofmetachars"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-requirenumberseparators"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-requirequotedheredocterminator"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-valuesandexpressions-requireuppercaseheredocterminator"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-variables-prohibitaugmentedassignmentindeclaration"
    )  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-variables-prohibitconditionaldeclarations"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitevilvariables")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitlocalvars")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitmatchvars")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitpackagevars")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitperl4packagenames")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitpunctuationvars")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitreusednames")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-prohibitunusedvariables")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-protectprivatevars")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-variables-requireinitializationforlocalvars"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-requirelexicalloopiterators")  # AUTO-CPAN2Spack
    provides(
        "perl-perl-critic-policy-variables-requirelocalizedpunctuationvars"
    )  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-variables-requirenegativeindices")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyconfig")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyfactory")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policylisting")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior-boolean")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior-enumeration")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior-integer")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior-string")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policyparameter-behavior-stringlist")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-profileprototype")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-statistics")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-testutils")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-theme")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-themelisting")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-userprofile")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-constants")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-dataconversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-mccabe")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-pod")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-pod-parseinteriorsequence")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-ppi")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-utils-perl")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-violation")  # AUTO-CPAN2Spack
    provides("perl-test-perl-critic-policy")  # AUTO-CPAN2Spack
    depends_on("perl-readonly@2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-which", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-io-string", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-task-weaken", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-node@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-pluggable@3.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-config-tiny@2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-utilities-statement@1.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document-file@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils@0.19:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-parser", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-spell@1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-utilities-node@1.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-token-quote-single@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-string-format@1.18:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-quotelike", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-regexp@0.27:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-plaintext", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-exception-class@1.23:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-select", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-b-keywords@1.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.42.4:", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-ppi-token-whitespace@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document@1.265:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-regexp-util@0.68:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-tidy", type="run")  # AUTO-CPAN2Spack
