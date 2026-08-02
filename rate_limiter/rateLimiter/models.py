from dataclasses import dataclass, field
from collections import deque
import threading


@dataclass(slots=True)
class Bucket:

    tokens: int

    last_refill: float
    
    # last_access:float

    lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
    )



@dataclass(slots=True)
class SlidingWindowState:

    timestamps: deque[float] = field(
        default_factory=deque
    )

    lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
    )

@dataclass(slots=True)
class FixedWindowState:

    request_count: int

    window_start: float

    lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
    )


@dataclass(slots=True)
class SlidingCounterState:

    previous_count: int

    current_count: int

    current_window_start: float

    lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
    )

