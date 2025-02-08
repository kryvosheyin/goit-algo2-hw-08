import time
import random
from typing import Dict


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.users_last_message_time = {}

    def can_send_message(self, user_id: str) -> bool:
        """
        Determines if a user is allowed to send a message based on the time since their last message.
        """

        current_time = time.time()

        if user_id in self.users_last_message_time:
            last_message_time = self.users_last_message_time[user_id]
            if current_time - last_message_time < self.min_interval:
                return False
        return True

    def record_message(self, user_id: str) -> bool:
        """
        Records a message for the user if allowed by the rate limiter.

        """

        if self.can_send_message(user_id):
            current_time = time.time()
            self.users_last_message_time[user_id] = current_time
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Calculates the time remaining until a user is allowed to send the next message.
        """

        current_time = time.time()

        if user_id in self.users_last_message_time:
            last_message_time = self.users_last_message_time[user_id]
            remaining_time = self.min_interval - (current_time - last_message_time)
            return max(0, remaining_time)

        return 0


def test_throttling_limiter():
    """Simulate a message stream with rate limiting."""
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Simulating Message Flow (Throttling) ===")
    for message_id in range(1, 11):
        user_id = str(message_id % 5 + 1)
        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)

        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}"
        )

        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 10 seconds...")
    time.sleep(10)

    print("\n=== Sending Another Round of Messages ===")
    for message_id in range(11, 21):
        user_id = str(message_id % 5 + 1)
        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)

        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}"
        )

        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()
