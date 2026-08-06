import pytest

from loadBalancer.least_connection import LeastConnectionStrategy
from loadBalancer.server import Server
from loadBalancer.routing_strategy import RoutingStrategy

@pytest.fixture
def strategy()->LeastConnectionStrategy:
    return LeastConnectionStrategy()


@pytest.fixture
def servers():
    return [
        Server("s1", "localhost", 8001),
        Server("s2", "localhost", 8002),
        Server("s3", "localhost", 8003),
    ]


def test_returns_only_server(strategy):
    server = Server("s1", "localhost", 8001)

    selected = strategy.select_server([server])

    assert selected is server


def test_raises_when_no_servers(strategy):
    with pytest.raises(ValueError):
        strategy.select_server([])


# def test_selects_server_with_least_connections(strategy, servers):
#     strategy.choose_server_test(servers[0])
#     strategy.choose_server_test(servers[0])

#     strategy.choose_server_test(servers[2])

#     selected = strategy.select_server(servers)

#     assert selected is servers[1]

def test_multiple_requests_are_distributed(strategy, servers):
    first = strategy.select_server(servers)
    second = strategy.select_server(servers)
    third = strategy.select_server(servers)

    assert first is servers[0]
    assert second is servers[1]
    assert third is servers[2]

    
def test_select_server_reserves_connection(strategy, servers):
    selected = strategy.select_server(servers)

    next_selected = strategy.select_server(servers)

    assert selected is servers[0]
    assert next_selected is servers[1]


def test_request_completion_releases_connection(strategy, servers):
    first = strategy.select_server(servers)
    second = strategy.select_server(servers)

    strategy.on_request_finished(first)

    third = strategy.select_server(servers)

    assert first is servers[0]
    assert second is servers[1]
    assert third is servers[0]


def test_returns_first_server_when_connections_are_equal(strategy, servers):
    selected = strategy.select_server(servers)

    assert selected is servers[0]