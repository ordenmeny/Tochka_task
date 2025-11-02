import copy
import sys
from collections import deque, defaultdict


def can_isolate(network: defaultdict, virus_position: str) -> tuple[str, bool]:
    free_steps = 0
    first_step = ""

    def bfs_find_next_step(start_node: str) -> tuple[str, str, int]:
        visited_nodes = {start_node}
        parents = {start_node: None}
        queue = deque([(start_node, 0)])

        while queue:
            current_node, distance = queue.popleft()
            for neighbor in sorted(network[current_node]):
                if neighbor in visited_nodes:
                    continue
                visited_nodes.add(neighbor)
                parents[neighbor] = current_node

                # нашли шлюз
                if neighbor.isupper():
                    pre_gateway_node = current_node
                    total_distance = distance + 1
                    first_move = pre_gateway_node
                    while (
                        parents[first_move] != start_node
                        and parents[first_move] is not None
                    ):
                        first_move = parents[first_move]
                    return first_move, pre_gateway_node, total_distance

                queue.append((neighbor, distance + 1))
        return None, None, None

    while True:
        next_first, target_node, dist_to_gate = bfs_find_next_step(virus_position)
        if not target_node:
            return first_step, True
        if first_step == "":
            first_step = next_first

        gateways_connected = sum(1 for n in network[target_node] if n.isupper())
        free_steps += dist_to_gate - gateways_connected - 1

        if free_steps < 0:
            return "", False

        virus_position = target_node
        connected_gates = [n for n in network[target_node] if n.isupper()]

        for gate in connected_gates:
            for neighbor in network[gate]:
                network[neighbor].remove(gate)
            network[gate] = set()


def solve(edges: list[tuple[str, str]]) -> list[str]:
    result = []
    virus_position = "a"

    graph = defaultdict(set)
    for n1, n2 in edges:
        graph[n1].add(n2)
        graph[n2].add(n1)

    candidate_edges = sorted(
        [sorted(edge) for edge in edges if edge[0].isupper() or edge[1].isupper()]
    )

    while candidate_edges:
        for edge_pair in candidate_edges:
            simulated_graph = copy.deepcopy(graph)
            simulated_graph[edge_pair[0]].remove(edge_pair[1])
            simulated_graph[edge_pair[1]].remove(edge_pair[0])

            next_virus_pos, is_safe = can_isolate(simulated_graph, virus_position)
            if is_safe:
                result.append(edge_pair[0] + "-" + edge_pair[1])
                candidate_edges.remove(edge_pair)
                virus_position = next_virus_pos
                graph[edge_pair[0]].remove(edge_pair[1])
                graph[edge_pair[1]].remove(edge_pair[0])
                break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition("-")
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
