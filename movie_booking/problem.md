# Movie Ticket Booking System

## Problem Statement

Design and implement an object-oriented Movie Ticket Booking System.

The system should allow users to:

-   Discover movies and their shows.
-   Select a movie, theatre, screen, and show.
-   View seat availability for a specific show.
-   Temporarily hold one or more seats.
-   Make a payment and confirm a booking.
-   Cancel a confirmed booking subject to a cancellation policy.
-   Release seats when a hold expires, payment fails, or a booking is
    cancelled.

The system must correctly handle concurrent users attempting to book the
same seat.

------------------------------------------------------------------------

## Functional Requirements

### Movie and Theatre Management

-   A `MovieComplex` contains multiple `Theatre` objects.
-   A `Theatre` contains multiple `Screen` objects.
-   A `Screen` contains a fixed physical seat configuration.
-   A `Seat` has a unique ID within its screen and a seat type such as:
    -   Regular
    -   Premium
    -   Recliner

### Show Management

A `Show` represents:

-   A movie
-   A screen
-   A start time
-   An end time

A screen cannot host overlapping shows.

Back-to-back shows are allowed:

``` text
18:00 ───── 21:00
              21:00 ───── 23:00
```

Overlapping shows must be rejected.

### Seat Availability

Physical seats belong to a screen and are independent of show-specific
availability.

For every show, create a separate `ShowSeat` for each physical seat.

``` text
Screen
  └── Seat A1

Show 1
  └── ShowSeat(A1, AVAILABLE)

Show 2
  └── ShowSeat(A1, BOOKED)
```

A `ShowSeat` maintains:

-   Physical seat reference
-   Status
-   Holder
-   Hold expiry

Possible states:

``` text
AVAILABLE
HELD
BOOKED
```

### Seat Holding

Users can temporarily hold multiple seats.

A hold has an expiry time.

The complete hold request must be atomic:

``` text
A1 = AVAILABLE
A2 = AVAILABLE
A3 = BOOKED

Request: A1, A2, A3

Result:
A1 = AVAILABLE
A2 = AVAILABLE
A3 = BOOKED
```

No partial hold is allowed.

### Booking

Booking flow:

``` text
Select seats
    ↓
Hold seats
    ↓
Payment
    ↓
Confirm seats
    ↓
Create confirmed booking
```

A booking contains:

-   Booking ID
-   User ID
-   Show ID
-   Seat IDs
-   Amount
-   Payment ID
-   Booking status

### Payment

Payment must be abstracted behind a `PaymentProcessor`.

The system must support:

-   Payment
-   Refund

Actual payment gateways are outside the scope of this LLD.

### Cancellation

A confirmed booking can be cancelled if allowed by the cancellation
policy.

Cancellation flow:

``` text
CONFIRMED
    ↓
Validate cancellation policy
    ↓
Refund payment
    ↓
Release booked seats
    ↓
CANCELLED
```

If cancellation validation fails, there must be no state mutation.

------------------------------------------------------------------------

## Concurrency Requirements

The system must guarantee that two users cannot acquire the same seat
simultaneously.

For example:

``` text
User A ──┐
         ├── A1
User B ──┘
```

Exactly one request should succeed.

`SeatInventory` owns the mutable show-specific seat state and uses a
lock to synchronize:

-   Seat viewing
-   Seat holding
-   Seat confirmation
-   Seat release

The lock must only cover the critical state operation.

It must **not** be held during external payment calls.

------------------------------------------------------------------------

## Expired Holds

Hold expiry is handled lazily.

When a seat is accessed:

``` text
HELD + expiry <= now
        ↓
AVAILABLE
```

No background scheduler is required for this LLD.

------------------------------------------------------------------------

## Failure and Compensation

Payment and seat inventory cannot participate in one real ACID
transaction because payment is an external dependency.

If payment fails:

``` text
HELD
  ↓
payment FAILED
  ↓
AVAILABLE
```

If payment succeeds but seat confirmation fails:

``` text
HELD
  ↓
payment SUCCESS
  ↓
confirmation FAILED
  ↓
REFUND
  ↓
AVAILABLE
```

A booking is created only after successful seat confirmation.

Refund failure is treated as a critical compensation failure rather than
pretending the external operation can be rolled back synchronously.

------------------------------------------------------------------------

## Non-Functional / Design Requirements

-   Use object-oriented design.
-   Keep domain objects focused on their responsibilities.
-   Encapsulate mutable seat state.
-   Avoid exposing mutable internal `ShowSeat` objects directly.
-   Keep payment implementation replaceable.
-   Keep cancellation rules replaceable.
-   Ensure multi-seat operations are atomic.
-   Keep concurrency boundaries explicit.

------------------------------------------------------------------------

## Out of Scope

The following are intentionally excluded:

-   Authentication and authorization
-   Real database
-   REST APIs
-   Actual payment gateway integration
-   Distributed locking
-   Distributed transactions
-   Notifications
-   Search indexing
-   Recommendation systems
-   Microservice architecture
-   Background hold-expiry workers

------------------------------------------------------------------------

## Core Domain Model

``` text
MovieComplex
    └── Theatre
          └── Screen
                └── Seat
```

``` text
Movie + Screen + Time
          ↓
         Show
          ↓
    SeatInventory
          ↓
       ShowSeat
          ↓
       Seat
```

``` text
BookingService
    ├── Show
    ├── SeatInventory
    ├── PaymentProcessor
    ├── CancellationPolicy
    └── Booking
```

------------------------------------------------------------------------

## Responsibilities

### `Seat`

Represents immutable physical seat configuration.

``` text
id
seat_type
```

### `Screen`

Owns physical seats and the screen's show schedule.

Responsibilities:

-   Store seats
-   Check schedule conflicts
-   Add shows

### `Theatre`

Owns screens.

### `MovieComplex`

Owns theatres.

### `Movie`

Represents movie metadata.

### `Show`

Represents a particular screening of a movie on a screen.

Contains:

-   Movie
-   Screen
-   Start/end time
-   `SeatInventory`

### `ShowSeat`

Represents the state of one physical seat for one particular show.

### `SeatInventory`

Owns show-specific seat state and concurrency.

Responsibilities:

-   View seat states
-   Hold seats
-   Confirm seats
-   Release held seats
-   Release booked seats
-   Handle hold expiry

### `Booking`

Represents a confirmed reservation.

### `BookingService`

Coordinates the booking and cancellation workflows.

### `PaymentProcessor`

Abstracts payment and refund operations.

### `CancellationPolicy`

Determines whether a booking can be cancelled.

------------------------------------------------------------------------

## Important Design Decisions

### Why `ShowSeat` instead of mutating `Seat`?

A physical seat is shared across many shows.

``` text
A1 on 18:00 show → BOOKED
A1 on 21:00 show → AVAILABLE
```

Therefore availability belongs to `(Show, Seat)`, not to `Seat`.

### Why a map for show seats?

`SeatInventory` stores:

``` text
seat_id → ShowSeat
```

This provides direct lookup when users request specific seats.

### Why no Prototype Pattern?

The system does not need object cloning.

We are reusing a physical seat configuration while maintaining
independent show-specific state. That is a modeling/ownership problem,
not a cloning problem.

### Why `SeatInventory`?

Without it, `Show` would be responsible for both:

-   Representing a movie screening
-   Managing concurrent seat state

Separating inventory makes the concurrency boundary explicit.

### Why `BookingService` instead of `Orchestrator`?

`BookingService` is the domain-specific orchestration layer. A generic
`Orchestrator` class would not add useful responsibility.

------------------------------------------------------------------------

## State Machines

### Seat

``` text
AVAILABLE
    ↓
HELD
   /   /   expiry cancel
  \   /
   ↓ ↓
AVAILABLE

HELD
  ↓
BOOKED

BOOKED
  ↓ cancellation
AVAILABLE
```

### Booking

``` text
CONFIRMED
    ↓
CANCELLED
```

A failed booking is never persisted as a `Booking`; the booking object
is created only after successful seat confirmation.

------------------------------------------------------------------------

## Test Requirements

The implementation should test at least:

1.  Show creates one `ShowSeat` per physical seat.
2.  All show seats initially start as `AVAILABLE`.
3.  Overlapping shows are rejected.
4.  Back-to-back shows are allowed.
5.  Available seats can be held.
6.  A held seat cannot be acquired by another user.
7.  Multi-seat hold is atomic.
8.  Only the holder can confirm seats.
9.  Hold expiry makes seats available again.
10. Successful payment produces a confirmed booking.
11. Payment failure releases held seats.
12. Payment succeeds but seat confirmation fails → payment is refunded.
13. Cancellation succeeds when allowed.
14. Cancellation after the show starts is rejected without mutation.
15. Cancellation refunds payment and releases booked seats.
16. Concurrent attempts to book the same seat result in exactly one
    success.

------------------------------------------------------------------------

## Key Invariants

The following must always hold:

### Seat ownership

``` text
A physical seat can have at most one active holder for a show.
```

### Booking

``` text
A confirmed booking owns all of its seats.
```

### Atomic hold

``` text
A multi-seat hold either holds every requested seat or none.
```

### Confirmation

``` text
Only the user who owns a valid hold can confirm it.
```

### Cancellation

``` text
A booking that is successfully cancelled releases all of its seats.
```

### Concurrency

``` text
Concurrent requests for the same show + seat
→ exactly one successful acquisition.
```
