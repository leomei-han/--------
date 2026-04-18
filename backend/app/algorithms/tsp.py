from __future__ import annotations

from itertools import combinations

from app.algorithms.graph import Graph


def held_karp(graph: Graph, start: str, nodes: list[str], strategy: str, transport_mode: str) -> tuple[list[str], float]:
    all_nodes = [start] + nodes
    distances: dict[tuple[str, str], float] = {}
    paths: dict[tuple[str, str], list[str]] = {}
    for source in all_nodes:
        for target in all_nodes:
            if source == target:
                continue
            path, cost = graph.shortest_path(source, target, strategy=strategy, transport_mode=transport_mode)
            distances[(source, target)] = cost
            paths[(source, target)] = path

    dp: dict[tuple[frozenset[str], str], tuple[float, str | None]] = {}
    for node in nodes:
        dp[(frozenset([node]), node)] = (distances[(start, node)], start)

    for size in range(2, len(nodes) + 1):
        for subset in combinations(nodes, size):
            subset_set = frozenset(subset)
            for last in subset:
                prev_subset = subset_set - {last}
                best = (float("inf"), None)
                for prev in prev_subset:
                    prev_cost, _ = dp[(prev_subset, prev)]
                    candidate = prev_cost + distances[(prev, last)]
                    if candidate < best[0]:
                        best = (candidate, prev)
                dp[(subset_set, last)] = best

    final_subset = frozenset(nodes)
    best_last = min(
        ((dp[(final_subset, node)][0] + distances[(node, start)], node) for node in nodes),
        key=lambda item: item[0],
    )

    ordered = [start]
    subset = final_subset
    current = best_last[1]
    trail = []
    while current is not None and subset:
        trail.append(current)
        _, prev = dp[(subset, current)]
        subset = subset - {current}
        current = prev if prev != start else None
    ordered.extend(reversed(trail))
    ordered.append(start)
    return ordered, best_last[0]


def nearest_neighbor_two_opt(graph: Graph, start: str, nodes: list[str], strategy: str, transport_mode: str) -> tuple[list[str], float]:
    remaining = set(nodes)
    route = [start]
    current = start
    total = 0.0
    while remaining:
        next_node = min(
            remaining,
            key=lambda node: graph.shortest_path(current, node, strategy=strategy, transport_mode=transport_mode)[1],
        )
        _, cost = graph.shortest_path(current, next_node, strategy=strategy, transport_mode=transport_mode)
        total += cost
        route.append(next_node)
        remaining.remove(next_node)
        current = next_node
    _, back_cost = graph.shortest_path(current, start, strategy=strategy, transport_mode=transport_mode)
    total += back_cost
    route.append(start)
    return route, total
