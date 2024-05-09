#!/usr/bin/env python3

import argparse
import json
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx

import lib


def get_records(base_bgp_dump, start_timestamp, end_timestamp, prefix):
    records = lib.read_bgpdump_file(
        bgpdump_file=base_bgp_dump,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    )

    pfx_routes = defaultdict(list)
    for rec in records:
        if rec["prefix"] == prefix and rec["type"] == "A":
            pfx_routes[rec["peer_asn"]] = rec["as-path"]
    return pfx_routes


def create_graph(pfx_records):

    assert len(pfx_records) > 2

    grafo = nx.DiGraph()

    # Adicionar nós e arestas ao grafo
    for origem, destinos in pfx_records.items():
        for i in range(len(destinos) - 1):
            origem_node = destinos[i]
            destino_node = destinos[i + 1]
            grafo.add_edge(origem_node, destino_node)

    return grafo


def draw_digraph(grafo, name):
    pos = nx.spring_layout(grafo)
    nx.draw(
        grafo,
        pos,
        with_labels=True,
        font_weight="bold",
        node_color="skyblue",
        node_size=100,
        font_size=10,
        edge_color="gray",
        linewidths=1,
        arrowsize=20,
    )

    plt.savefig(f"{name}.png")
    plt.clf()


def assert_reachable_asns(pfx_records, graph, status=""):
    reachable = []
    for c in pfx_records:
        for asn in pfx_records[c]:
            if asn not in reachable:
                reachable.append(asn)
    print("Number of ASNs that %s pfx was able to reach %i" % (status, len(reachable)))
    assert len(reachable) == graph.number_of_nodes()



def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--location",
        metavar="location",
        type=str,
        required=True,
        dest="location",
        help="Location where the experiments were deployed",
    )
    parser.add_argument(
        "--measurement",
        metavar="measurement",
        type=str,
        required=True,
        dest="measurement",
        help="Measurement run tag",
    )
    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()
    config_fn = parser.prog.replace(".py", "")

    with open(f"{config_fn}.json", "r") as cf:
        config_data = json.load(cf)

    bgp_file = config_data[args.measurement]["bgpdump"]

    start_timestamp = config_data[args.measurement][args.location]["start"]
    end_timestamp = config_data[args.measurement][args.location]["end"]

    non_invalid_pfx = get_records(
        bgp_file,
        start_timestamp,
        end_timestamp,
        config_data[args.measurement]["prefixes"]["non_invalid"],
    )
    invalid_pfx = get_records(
        bgp_file,
        start_timestamp,
        end_timestamp,
        config_data[args.measurement]["prefixes"]["invalid"],
    )

    non_invalid_graph = create_graph(non_invalid_pfx)
    invalid_graph = create_graph(invalid_pfx)

    assert_reachable_asns(non_invalid_pfx, non_invalid_graph, "NON_INVALID")
    assert_reachable_asns(invalid_pfx, invalid_graph,"INVALID")

    draw_digraph(non_invalid_graph, f"{args.location}_non_invalid")
    draw_digraph(invalid_graph, f"{args.location}_invalid")


if __name__ == "__main__":
    sys.exit(main())
