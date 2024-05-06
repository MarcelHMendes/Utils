#!/usr/bin/env python3

import argparse
import json
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dump",
        metavar="bgpdump_json",
        type=str,
        required=True,
        dest="bgpdump",
        help="Dump BGP (json format)",
    )
    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()

    file = open(args.bgpdump, "r")
    records = json.load(file)
    file.close()
    name = args.bgpdump.replace(".json", "")

    sorted_records = sorted(records, key=lambda x: x["timestamp"])

    with open(f"{name}_sorted.json", "w", encoding="utf-8") as fout:
        json.dump(sorted_records, fout, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    sys.exit(main())
