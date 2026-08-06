import pytest

from loadBalancer.weighted_round_robin import (
    WeightedRoundRobinStrategy,
)
from loadBalancer.server import Server


def create_servers():
    server_a = Server(
        server_id="A",
        host="localhost",
        port=8001,
        weight=1,
    )
    server_b = Server(
        server_id="B",
        host="localhost",
        port=8002,
        weight=2,
    )
    server_c = Server(
        server_id="C",
        host="localhost",
        port=8003,
        weight=3,
    )
    return server_a, server_b, server_c


def test_empty_server_list():
    strategy = WeightedRoundRobinStrategy()

    with pytest.raises(ValueError):
        strategy.select_server([])


def test_single_server_is_always_selected():
    strategy = WeightedRoundRobinStrategy()

    server = Server(
        server_id="A",
        host="localhost",
        port=8001,
        weight=5,
    )

    for _ in range(20):
        assert strategy.select_server([server]) is server


def test_smooth_weighted_round_robin_sequence():
    strategy = WeightedRoundRobinStrategy()

    server_a, server_b, server_c = create_servers()

    servers = [
        server_a,
        server_b,
        server_c,
    ]

    expected = [
        server_c,
        server_b,
        server_a,
        server_c,
        server_b,
        server_c,
    ]

    actual = [
        strategy.select_server(servers)
        for _ in range(6)
    ]

    assert actual == expected


def test_sequence_repeats_after_one_cycle():
    strategy = WeightedRoundRobinStrategy()

    server_a, server_b, server_c = create_servers()

    servers = [
        server_a,
        server_b,
        server_c,
    ]

    first_cycle = [
        strategy.select_server(servers)
        for _ in range(6)
    ]

    second_cycle = [
        strategy.select_server(servers)
        for _ in range(6)
    ]

    assert first_cycle == second_cycle


def test_request_distribution_matches_weights():
    strategy = WeightedRoundRobinStrategy()

    server_a, server_b, server_c = create_servers()

    servers = [
        server_a,
        server_b,
        server_c,
    ]
                        
    counts = {
        server_a: 0,
        server_b: 0,
        server_c: 0,
    }

    total_requests = 600

    for _ in range(total_requests):
        server = strategy.select_server(servers)
        counts[server] += 1

    assert counts[server_a] == 100
    assert counts[server_b] == 200
    assert counts[server_c] == 300


def test_removed_server_is_never_selected():
    strategy = WeightedRoundRobinStrategy()

    server_a, server_b, server_c = create_servers()

    servers = [
        server_a,
        server_b,
        server_c,
    ]

    for _ in range(10):
        strategy.select_server(servers)

    remaining = [
        server_a,
        server_c,
    ]

    for _ in range(20):
        selected = strategy.select_server(remaining)
        assert selected is not server_b


def test_on_request_finished_has_no_effect():
    strategy = WeightedRoundRobinStrategy()

    server_a, server_b, server_c = create_servers()

    servers = [
        server_a,
        server_b,
        server_c,
    ]

    before = strategy.select_server(servers)

    strategy.on_request_finished(before)

    after = strategy.select_server(servers)

    assert after is not None

def test_equal_weights_behave_like_round_robin():
    strategy = WeightedRoundRobinStrategy()

    server_a = Server("A", "localhost", 8001, weight=1)
    server_b = Server("B", "localhost", 8002, weight=1)
    server_c = Server("C", "localhost", 8003, weight=1)

    servers = [server_a, server_b, server_c]

    expected = [
        server_a,
        server_b,
        server_c,
        server_a,
        server_b,
        server_c,
    ]

    actual = [
        strategy.select_server(servers)
        for _ in range(6)
    ]

    assert actual == expected