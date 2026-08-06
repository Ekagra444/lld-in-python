from loadBalancer.server import Server,ServerStatus

def test_server_creation():
    server = Server(
        "server-1",
        "localhost",
        8080,
    )

    assert server.server_id == "server-1"
    assert server.host == "localhost"
    assert server.port == 8080
    assert server.status == ServerStatus.HEALTHY

def test_server_status_update():
    server = Server(
        "1",
        "localhost",
        8080,
    )

    server.set_status(ServerStatus.UNHEALTHY)

    assert (
        server.status
        == ServerStatus.UNHEALTHY
    )