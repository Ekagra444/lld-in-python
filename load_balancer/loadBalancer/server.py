from __future__ import annotations

from enum import Enum, auto
from threading import Lock

class ServerStatus(Enum):
    HEALTHY=auto()
    UNHEALTHY=auto()

class Server:
    def __init__(
            self,
            server_id:str,
            host:str,
            port:str,
            weight:int=1
        )->None:
        self._server_id = server_id
        self._host = host
        self._port = port
        self._status = ServerStatus.HEALTHY
        self._lock = Lock()
        if(weight<=0):
            raise ValueError('eight wmust be greater than 0')
        self._weight = weight

    @property
    def server_id(self)->str:
        return self._server_id

    @property
    def host(self)->str:
        return self._host

    @property
    def port(self)->int:
        return self._port

    @property
    def status(self)->ServerStatus:
        with self._lock:
            return self._status

    def set_status(self,status:ServerStatus)->None:
        with self._lock:
            self._status = status

    # Can lead to explosive number of classes as states increase
    # def mark_unhealthy(self)->None:
    #     self.set_status(ServerStatus.UNHEALTHY)

    # def is_healthy(self)->bool:
    #     return self._status == ServerStatus.HEALTHY

    def __repr__(self) -> str:
        return f"""Server(
            id={self.server_id},
            host={self.host},
            port={self.port},
            status={self.status.name}
        )"""

