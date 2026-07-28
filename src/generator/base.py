from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Base class for all entity generators."""

    @abstractmethod
    def generate(self):
        """Generate records."""
        raise NotImplementedError