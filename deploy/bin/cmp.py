import yaml


def load(team=""):
    fn = "deploy/environments/applications.yaml"
    if team:
        fn = f"deploy/environments/applications_{team}.yaml"
    with open(fn) as fd:
        data = yaml.load(fd)
        return set(data["spack"]["specs"])


ref = load()
new = set()
for t in "dke hpc ml nse nse_circuits science viz".split():
    new |= load(t)
for s in sorted(ref - new):
    print(s)
