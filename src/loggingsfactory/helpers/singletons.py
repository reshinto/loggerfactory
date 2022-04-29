"""Keep track of total number of logs called"""


class LogCounter:
    """Keep track of total number of logs called"""

    def __init__(self) -> None:
        """
        Initialize counter variable

        - self.counter: int = this is used to track the number of log or async_log calls.
        """
        self.counter: int = 0

    def increment(self) -> None:
        """Increment counter"""
        self.counter += 1


logcounter = LogCounter()
