from loadBalancer.round_robin import RoundRobinStrategy
from loadBalancer.server import Server,ServerStatus

def test_round_robin_sequence():
    strategy = RoundRobinStrategy()

    servers = [
        Server("A", "a", 1),
        Server("B", "b", 2),
        Server("C", "c", 3),
    ]

    assert strategy.select_server(servers).server_id == "A"
    assert strategy.select_server(servers).server_id == "B"
    assert strategy.select_server(servers).server_id == "C"
    assert strategy.select_server(servers).server_id == "A"

def test_round_robin_after_server_removal():
    strategy = RoundRobinStrategy()

    servers = [
        Server("A", "", 1),
        Server("B", "", 2),
        Server("C", "", 3),
    ]

    strategy.select_server(servers)
    strategy.select_server(servers)
    strategy.select_server(servers)

    servers.pop()

    assert (
        strategy.select_server(servers).server_id
        == "A"
    )