import sys
from typing import Dict

import yaml


def read_dotenv(file_name: str) -> Dict[str, str]:
    result = []
    with open(file_name, "r", encoding="utf-8") as fd:
        for field in fd:
            if field.strip()[0] == "#":
                continue

            data = field.strip("\n").split("=", 1)
            try:
                result.append((data[0], data[1]))
            except IndexError:
                print(f"Skipping bad value: {field}")

    return dict(result)


if __name__ == "__main__":
    dotenv = read_dotenv(sys.argv[1])
    if not dotenv:
        exit(0)

    with open(sys.argv[2], "r", encoding="utf-8") as fd:
        conf = yaml.load(fd, Loader=yaml.Loader)

    if "variables" not in conf:
        conf["variables"] = {}
    conf["variables"].update(dotenv)

    with open(sys.argv[2], "w", encoding="utf-8") as fd:
        yaml.dump(conf, fd, Dumper=yaml.Dumper)
