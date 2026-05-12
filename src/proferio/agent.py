from dataclasses import dataclass, field
from typing import List

from .tools import ToolRegistry


@dataclass
class AgentState:
    question: str
    thoughts: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    final_answer: str | None = None


class ReActController:
    def __init__(self, tool_registry: ToolRegistry, max_steps: int = 6):
        self.tools = tool_registry
        self.max_steps = max_steps

    def run(self, question: str, approval_callback=None):
        state = AgentState(question=question)
        q = question.lower()

        for i in range(self.max_steps):
            state.thoughts.append(f"Step {i+1}: decide best tool for progress")
            tools = self.tools.list_tools()
            if not tools:
                break
            tool = tools[i % len(tools)]
            for t in tools:
                name = t.name.lower()
                desc = t.description.lower()
                if any(k in q for k in ["policy", "source", "citation", "governance", "requirement"]) and "rag" in name:
                    tool = t
                    break
                if any(k in q for k in ["calculate", "math", "sum"]) and "calc" in name:
                    tool = t
                    break
            action = f"use_tool:{tool.name}"
            if approval_callback and not approval_callback(action):
                state.actions.append(f"denied:{action}")
                continue
            state.actions.append(action)
            obs = self.tools.call(tool.name, question)
            state.observations.append(obs[:800])
            if "insufficient" not in obs.lower() and len(obs.strip()) > 30:
                state.final_answer = obs
                break

        if not state.final_answer:
            state.final_answer = "Insufficient evidence from available tools."

        return state
