from dataclasses import dataclass
from typing import Callable, Dict


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[str], str]


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def call(self, name: str, arg: str) -> str:
        return self._tools[name].fn(arg)

    def list_tools(self):
        return list(self._tools.values())
