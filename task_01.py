import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        
        self.window_size = window_size
        self.max_requests = max_requests
        self.queue = deque()

    def _cleanup_window(self, user_id: str, current_time: float) -> None:

        """Removes outdated messages from the queue."""


        self.queue = deque([record for record in self.queue if (user_id not in record or current_time - record[user_id] <= self.window_size)])

    def can_send_message(self, user_id: str) -> bool:
        """Checks if the user can send a message in the current time window."""

        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return sum(1 for record in self.queue if user_id in record) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """Records a new message if allowed."""
        if self.can_send_message(user_id):
            self.queue.append({user_id: time.time()})
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Calculates how long until the user can send the next message."""
        current_time = time.time()
        for record in self.queue:
            if user_id in record:
                return self.window_size - (current_time - record.get(user_id, 0))
        return 0


def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print("\n=== Simulating Message Flow ===")
    for message_id in range(1, 11):
        user_id = str(message_id % 5 + 1) 

        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")

        time.sleep(random.uniform(0.1, 1.0))  

    print("\nWaiting 4 seconds...\n")
    time.sleep(4)

    print("\n=== New Messages After Waiting ===")
    for message_id in range(11, 21):
        user_id = str(message_id % 5 + 1)
        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()