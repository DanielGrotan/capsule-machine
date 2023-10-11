from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Command[T]:
    description: str
    function: Callable[[T], None]
    quit_after_execution: bool = field(default=False)

    def execute(self, command_input: T) -> None:
        self.function(command_input)
