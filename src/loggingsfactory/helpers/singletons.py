"""Keep track of total number of logs called"""
import loguru


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


class SetupLoguru:
    """Setup loguru library"""

    def __init__(self) -> None:
        """
        - self.logger: loguru.Logger = this is the Loguru library logger instance.

        - self.logger.add("logs/logfile.log") = this auto creates the log folder and logfile.log inside it.
                                                auto creation happens when the logger is initialized,
                                                or when unit tests are run.
        """
        self.logger: loguru.Logger = loguru.logger
        self.logger.add("logs/logfile.log")


logger = SetupLoguru().logger
