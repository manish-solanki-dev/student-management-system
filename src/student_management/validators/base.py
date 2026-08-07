from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Validator(ABC, Generic[T]):
    """Define the contract for value validators."""

    @abstractmethod
    def validate(self, value: T) -> None:
        """Validate a value or raise an appropriate exception."""
        raise NotImplementedError
