import pytest
from loadBalancer.load_balancer import LoadBalancer
from loadBalancer.round_robin import RoundRobinStrategy
from loadBalancer.server import Server,ServerStatus
from loadBalancer.exceptions import NoHealthyServersException

def test_register_server():
    lb = LoadBalancer(
        RoundRobinStrategy()
    )

    server = Server(
        "1",
        "localhost",
        8080,
    )

    lb.register_server(server)

    assert lb.get_next_server() == server


def test_unhealthy_servers_are_skipped():
    lb = LoadBalancer(
        RoundRobinStrategy()
    )

    s1 = Server("A", "", 1)
    s2 = Server("B", "", 2)

    s2.set_status(ServerStatus.UNHEALTHY)

    lb.register_server(s1)
    lb.register_server(s2)

    assert (
        lb.get_next_server().server_id
        == "A"
    )

    assert (
        lb.get_next_server().server_id
        == "A"
    )



def test_no_healthy_servers():
    lb = LoadBalancer(
        RoundRobinStrategy()
    )

    server = Server("A", "", 1)
    server.set_status(ServerStatus.UNHEALTHY)

    lb.register_server(server)

    with pytest.raises(
        NoHealthyServersException
    ):
        lb.get_next_server()

def test_empty_load_balancer():
    lb = LoadBalancer(
        RoundRobinStrategy()
    )

    with pytest.raises(
        NoHealthyServersException
    ):
        lb.get_next_server()