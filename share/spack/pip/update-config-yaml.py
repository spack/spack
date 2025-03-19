import yaml
import argparse
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input config.yaml", action="store", default=sys.stdin)
    parser.add_argument("-o", "--output", type=str, help="Output config.yaml", action="store", default=sys.stdout)
    args = parser.parse_args()

    if args.input != sys.stdin:
        with open(args.input, 'r') as f:
            in_str = f.read()
    else:
        in_str = sys.stdin.read(in_str)

    config_yaml = yaml.safe_load(in_str)
    config_yaml['config']['install_tree']['root'] = '$per_spack_user'

    out_str = yaml.dump(config_yaml)
    if args.output != sys.stdout:
        with open(args.output, 'w') as f:
            f.write(out_str)
    else:
        sys.stdout.write(out_str)
