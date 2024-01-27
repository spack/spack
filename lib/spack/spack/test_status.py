import enum

class TestStatus(enum.Enum):
    """Names of different stand-alone test states."""

    NO_TESTS = -1
    SKIPPED = 0
    FAILED = 1
    PASSED = 2

    def __str__(self):
        return f"{self.name}"

    def lower(self):
        name = f"{self.name}"
        return name.lower()
