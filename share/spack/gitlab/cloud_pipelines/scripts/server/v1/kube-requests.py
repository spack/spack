#!/bin/env python

import json
import sys
import os

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

if __name__ == "__main__":
    data = json.loads(sys.argv[1])

    static = {"packages": {}, "mapping": {}}
    with open(os.path.join(script_dir, "static-mapping.json"), "r") as fd:
        static = json.load(fd)

    reponse = {}
    for obj in data:
        mapping_name = static["packages"].get(obj["package"]["name"], "default")
        mapping = static["mapping"].get(mapping_name)
        if mapping:
            reponse[obj["hash"]] = mapping

    print(json.dumps(reponse))
