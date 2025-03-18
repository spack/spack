import re
import sys
import toml
import argparse

def update_value(fqn, value):
    if fqn == '.project.name':
        new_val = 'spack-package-manager-mlcurry'
    elif fqn == '.project.scripts.spack':
        new_val = 'spack.' + value
    elif re.match(r'^(lib|bin|var)/spack', value):
        new_val = 'spack/' + value
    elif re.match(r'^\./(lib|bin|var)/spack', value):
        new_val = './spack/' + value[2:]
    elif fqn == '.tool.hatch.build.targets.wheel.include':
        if value[0] == '/':
            new_val = '/spack' + value
        else:
            new_val = '/spack/' + value
    else:
        print('Not changed:')
        print(fqn)
        print('    ', value)
        print()
        return value

    print('Updated', fqn)
    print('   ', value)
    print('   ', new_val)
    return new_val

def should_delete(fqn):
    #if fqn in ['.tool.isort', '.tool.black', '.tool.mypy',
    #           '.tool.coverage', '.tool.ruff']:
    #    return True
    return False

def descend(coll, fqn=''):
    # Get down to strings. Fuzzify fqn if necessary.
    to_delete = []
    if type(coll) == dict:
        for k,v in coll.items():
            new_fqn = fqn + '.' + k
            if type(v) in [int, bool]:
                pass
            elif type(v) == str:
                coll[k] = update_value(new_fqn, v)
            else:
                if should_delete(new_fqn):
                    print('Marking for deletion:')
                    print(coll[k])
                    to_delete.append(k)
                else:
                    descend(coll[k], new_fqn)
    elif type(coll) == list:
        for idx in range(len(coll)):
            #new_fqn = fqn + '[' + str(idx) + ']'
            new_fqn = fqn
            if type(coll[idx]) == str:
                #print(new_fqn, coll[idx])
                coll[idx] = update_value(new_fqn, coll[idx])
            elif type(coll[idx]) in [int, bool]:
                pass
            else:
                descend(coll[idx], new_fqn)
    else:
        print(type(coll))
        assert(False)
    for section in to_delete:
        del coll[section]


def process_keys2(coll, fqn=''):
    # fqn is only used for testing, and is not updated when descending
    # into a coll. This can turn a list into strings, so don't depend
    # on the type when testing fqn.
    if fqn == '.tool.ruff.extend-include':
        print('Seen')
        print(coll)
        print(type(coll[0]))

    if type(coll) == dict:
        for key, value in coll.items():
            new_fqn = fqn + "." + key
            if type(value) == list:
                old_value = value
                new_value = []
                for idx in range(len(value)):
                    if type(value[idx]) != str:
                        process_keys2(value, new_fqn)
                        continue
                    new_value.append(update_value(new_fqn, value[idx]))
                if new_value != value:
                    print('Update', new_fqn)
                    print('   ', old_value)
                    print('   ', new_value)
            elif type(value) == str:
                    new_value = update_value(new_fqn, value)
                    if new_value != value:
                        print('Update', new_fqn)
                        print('   ', value)
                        print('   ', new_value)
            elif type(value) == dict:
                process_keys2(value, new_fqn)
            elif type(value) in [bool, int]:
                pass
            else:
                print(new_fqn, 'did not trigger.')
                print(type(coll), type(value))

def process_keys(d, fqn=''):
    for key, value in d.items():
        new_fqn = fqn + "." + key
        if type(value) == dict:
            process_keys(value, new_fqn)
        else:
            print('Old entry:', new_fqn, '=', value)
            if new_fqn == '.project.scripts.spack':
                d[key] = 'spack.' + value
                print('Update:   ', new_fqn, '=', d[key])
            if new_fqn in ['.tool.hatch.version.path']:
                d[key] = 'spack/' + value
                print('Update:   ', new_fqn, '=', d[key])
            if new_fqn in ['.tool.hatch.build.targets.wheel.include']:
                for idx in range(len(d[key])):
                    prepend = '/spack'
                    if d[key][idx][0] != '/':
                        prepend += '/'
                    d[key][idx] = prepend + d[key][idx]
                print('Update:   ', new_fqn, '=', d[key])
            if type(value) == str and re.search(r"^\./bin/", value) is not None:
                d[key] = d[key].replace('./bin/', './spack/bin/', 1)
                print('Update:   ', new_fqn, '=', d[key])
            if type(value) == str and re.search(r"^bin/spack", value) is not None:
                d[key] = d[key].replace('bin/spack', 'spack/bin/spack', 1)
                print('Update:   ', new_fqn, '=', d[key])
            if type(value) == str and re.search(r"^lib/spack", value) is not None:
                d[key] = d[key].replace('lib/spack', 'spack/lib/spack', 1)
                print('Update:   ', new_fqn, '=', d[key])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input pyproject.toml", action="store", default=sys.stdin)
    parser.add_argument("-o", "--output", type=str, help="Output pyproject.toml", action="store", default=sys.stdout)
    args = parser.parse_args()
    print(args)

    spack_toml = toml.load(args.input)
    #for k,v in spack_toml.items():
    #    print(k, v)
    #    if type(v) == dict:
    #        print('Subdict:')
    #process_keys2(spack_toml)
    descend(spack_toml)
    out_str = toml.dumps(spack_toml)
    if args.output != sys.stdout:
        with open(args.output, 'w') as f:
            f.write(out_str)
    else:
        sys.stdout.write(out_str)

