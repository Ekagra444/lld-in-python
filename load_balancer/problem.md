Low-Level Design Problem #2: Load Balancer
Problem Statement

Design and implement an in-memory Load Balancer capable of distributing incoming client requests across a pool of backend servers.

The load balancer should expose a simple API through which clients submit requests and receive the backend server selected to handle that request. The system must be designed to support multiple load balancing algorithms while remaining easily extensible for future routing strategies.

The implementation should maintain the health and availability status of backend servers and ensure that requests are routed only to healthy servers. It should also allow backend servers to be added to or removed from the system dynamically without interrupting request routing.

The design should be thread-safe, scalable, and follow sound object-oriented design principles such as SOLID, favoring composition over inheritance where appropriate. The solution should emphasize clean abstractions so that introducing a new routing algorithm requires minimal or no modification to existing code.

The implementation should be suitable for demonstrating production-quality software engineering practices, including proper encapsulation, concurrency handling, and comprehensive unit testing.