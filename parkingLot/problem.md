# Parking Lot — Low-Level Design Problem

## 1. Problem Statement

Design a thread-safe, extensible **Parking Lot System** that manages parking of different types of vehicles across multiple floors and parking spots.

The system should support vehicle entry and exit, parking spot allocation, ticket generation, and parking fee calculation.

The design should be extensible enough to support different parking allocation and pricing strategies without requiring changes to the core parking lot workflow.

---

## 2. Vehicles

The parking lot supports the following vehicle types:

* Motorcycle
* Car
* Truck

Each vehicle has:

* A unique registration number
* A vehicle type

The vehicle type is used when determining whether a vehicle can fit into a particular parking spot.

---

## 3. Parking Lot Structure

A parking lot consists of multiple floors.

Each floor contains multiple parking spots.

The parking lot hierarchy is:

```text
Parking Lot
    |
    +-- Floor
    |     |
    |     +-- Parking Spot
    |     +-- Parking Spot
    |     +-- ...
    |
    +-- Floor
          |
          +-- Parking Spot
          +-- Parking Spot
          +-- ...
```

The system should support:

* Adding floors to a parking lot.
* Adding parking spots to a floor.
* Preventing duplicate floor IDs within a parking lot.
* Preventing duplicate spot IDs within a floor.

For this version, the physical parking lot configuration is established before normal parking operations begin.

---

## 4. Parking Spots

The parking lot supports different types of parking spots:

* Motorcycle spot
* Compact spot
* Large spot

A parking spot can either be:

* Available
* Occupied

A parking spot must determine whether a given vehicle is compatible with it.

A vehicle cannot be parked in an incompatible spot.

An occupied spot cannot be occupied by another vehicle.

An empty spot cannot be vacated.

---

## 5. Concurrent Parking

The system must be thread-safe.

Multiple vehicles may attempt to park concurrently.

The following operation must be atomic:

```text
Check whether the spot is available
        +
Claim the spot
```

Two concurrent requests must never successfully occupy the same parking spot.

If a parking allocation becomes invalid because another thread claims the selected spot first, the parking operation should be able to retry using the configured retry policy.

---

## 6. Parking Spot Allocation

The system should not hardcode parking allocation logic inside the parking service.

Instead, parking allocation must be represented using a strategy abstraction.

The allocation strategy receives:

* The parking lot
* The vehicle

and determines an appropriate parking location.

The allocation result must identify:

* The selected floor
* The selected parking spot

The initial implementation should provide a **First Available** allocation strategy.

The strategy should:

1. Traverse floors in their configured order.
2. Traverse spots in their configured order.
3. Ignore occupied spots.
4. Ignore spots incompatible with the vehicle.
5. Return the first suitable location.
6. Return no allocation if no suitable spot exists.

The design should allow additional allocation strategies to be introduced without modifying `ParkingService`.

---

## 7. Parking Ticket

When a vehicle successfully parks, the system generates a parking ticket.

A ticket contains:

* Unique ticket ID
* Vehicle
* Floor ID
* Spot ID
* Entry time
* Exit time, once the vehicle leaves
* Parking fee, once calculated

A newly created ticket is active.

The ticket lifecycle is:

```text
Ticket Created
      |
      v
Vehicle Parked
      |
      v
Exit Time Recorded
      |
      v
Fee Calculated
      |
      v
Fee Recorded
      |
      v
Ticket Closed
```

A ticket must not have its exit time set more than once.

A ticket must not have its fee set more than once.

A fee cannot be recorded before an exit time has been recorded.

---

## 8. Active Parking Sessions

The system must maintain information about currently active parking sessions.

For every active ticket, the system must be able to efficiently identify the parking spot occupied by that ticket.

An active parking session therefore represents the relationship between:

```text
Parking Ticket
      +
Occupied Parking Spot
```

Active sessions are indexed by ticket ID.

---

## 9. Vehicle Exit

When a vehicle exits, the system receives its ticket ID.

The system should:

1. Locate the active parking session.
2. Record the ticket's exit time.
3. Calculate the parking fee.
4. Store the calculated fee on the ticket.
5. Release the occupied parking spot.
6. Remove the active parking session.
7. Return the calculated fee.

Attempting to exit using an unknown or inactive ticket ID should fail.

---

## 10. Pricing

Parking fee calculation must be separated from the parking service.

The system should use a pricing strategy abstraction.

The pricing strategy receives a parking ticket and calculates the fee based on the completed parking duration and vehicle information.

The initial implementation should provide an **Hourly Pricing Strategy**.

The initial pricing rules are:

| Vehicle Type |        Rate |
| ------------ | ----------: |
| Motorcycle   |  ₹20 / hour |
| Car          |  ₹50 / hour |
| Truck        | ₹100 / hour |

Billing is based on started hours.

For example:

```text
1–60 minutes     → 1 hour
61–120 minutes   → 2 hours
121–180 minutes  → 3 hours
```

A minimum charge of one hour applies.

Monetary calculations should avoid floating-point arithmetic.

The pricing strategy must be replaceable without modifying the parking service.

---

## 11. Parking Service

The parking service acts as the primary application-level coordinator.

It should expose operations for:

### Park

```text
park(vehicle)
```

The operation should:

1. Request a parking allocation from the allocation strategy.
2. Attempt to atomically claim the selected spot.
3. Retry when the selected spot has been claimed concurrently.
4. Generate a unique ticket after successfully claiming a spot.
5. Create an active parking session.
6. Return the ticket.

If no suitable spot exists, the operation should fail.

If all configured retry attempts are exhausted because of concurrent allocation conflicts, the operation should fail.

### Exit

```text
exit(ticket_id)
```

The operation should execute the exit workflow described above and return the calculated fee.

---

## 12. Thread Safety Requirements

The following shared state must be protected against concurrent modification:

### Parking spot state

The transition:

```text
Available → Occupied
```

must be atomic.

Likewise:

```text
Occupied → Available
```

must be thread-safe.

### Active parking sessions

Concurrent parking and exit requests must not corrupt the active-session state.

The system must preserve the invariant:

```text
Every active ticket corresponds to exactly one
active parking session and one occupied parking spot.
```

---

## 13. Extensibility Requirements

The design should allow new behavior to be introduced without modifying the core `ParkingService`.

The following should be replaceable independently:

### Parking allocation

Examples:

```text
First Available
Nearest Entrance
Least Occupied Floor
Vehicle-Specific Allocation
```

### Pricing

Examples:

```text
Hourly Pricing
Weekend Pricing
Dynamic Pricing
VIP Pricing
Vehicle-Specific Pricing
```

Adding a new allocation or pricing algorithm should require implementing the relevant strategy rather than modifying the existing service orchestration logic.

---

## 14. Constraints

The design should:

* Be thread-safe for concurrent parking and exit operations.
* Prevent double occupancy of a parking spot.
* Prevent parking incompatible vehicles.
* Maintain O(1) lookup of an active parking session by ticket ID.
* Keep allocation logic separate from orchestration.
* Keep pricing logic separate from orchestration.
* Preserve encapsulation of parking lot, floor, and spot collections.
* Avoid unnecessary data structures where sequential traversal is sufficient.
* Use appropriate domain-specific exceptions for domain failures.
* Use precise monetary representation for parking fees.

---

## 15. Expected Deliverable

Design and implement the system using appropriate object-oriented and design-pattern principles.

The implementation should include:

1. Vehicle model
2. Parking spot model
3. Parking floor model
4. Parking lot model
5. Parking ticket model
6. Active parking session model
7. Spot allocation result model
8. Parking allocation strategy
9. First Available allocation strategy
10. Pricing strategy
11. Hourly pricing strategy
12. Parking service
13. Appropriate domain exceptions
14. Unit tests
15. Concurrency tests

The implementation should demonstrate:

* Encapsulation
* Composition
* Strategy Pattern
* Separation of concerns
* Thread safety
* Explicit domain modeling
* Testable abstractions
* Extensibility
