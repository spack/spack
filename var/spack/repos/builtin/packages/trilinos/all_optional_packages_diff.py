try:
    from spack.spec import Spec
    spack.config.set("concretizer::reuse", False)
except:
    print("WARNING!: Call `spack python` rather than `python` directly")
    raise
import argparse
parser = argparse.ArgumentParser(description='Get variants equivalent to +all_optional_packages')
parser.add_argument('spec', help='variants to enable in Trilinos spec')
args = parser.parse_args()
assert args.spec[0]=="+", 'Variants in Trilinos spec must begin with +'
args.spec = 'trilinos' + args.spec
print(args)

def optional_vs_required(package):
    trilinos = Spec(package)
    ct = trilinos.concretized()
    trilinos_oe = Spec(package + '+all_optional_packages')
    ct_oe = trilinos_oe.concretized()
    on_with_oe = set()
    for key in ct_oe.variants.keys():
        if ct_oe.variants[key].value:
            on_with_oe.add(key)
    on_no_oe = set()
    for key in ct.variants.keys():
        if ct.variants[key].value:
            on_no_oe.add(key)
    return '+'+'+'.join((on_with_oe - on_no_oe) - set(['all_optional_packages']))

print("Gathering differences...")
diffs = optional_vs_required(args.spec)
print("The changes needed for {0} to be equivalent to setting +all_optional_packages are:".format(args.spec))
print(diffs)
