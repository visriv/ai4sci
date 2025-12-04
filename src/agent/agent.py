import json
from pathlib import Path
from typing import Dict, Any, List
import asyncio

from .llm_client import LLMClient
from .async_utils import gather_dict
from ..utils.logger import get_logger

logger = get_logger("Agent")


class RCAAgent:
    def __init__(self, llm_model, system_prompt_path, tools: dict, max_steps=4):
        self.llm = LLMClient(llm_model, host="http://host.docker.internal:11434")
        self.tools = tools
        self.max_steps = max_steps
        self.system_prompt = Path(system_prompt_path).read_text().strip()

        logger.info("[Agent] [Init] RCA Agent initialized")

    # -----------------------------
    # Build LLM message context
    # -----------------------------
    def _messages(self, run_summary: str, history: List[dict]):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": run_summary},
            *history
        ]

    # -----------------------------
    # Parse 1 or more tool calls
    # -----------------------------
    def _extract_tool_calls(self, text: str) -> Dict[str, dict]:
        """
        LLM format (example):
        TOOL_CALL:
        {"tool": "search_logs", "args": {"query": "..."}}
        TOOL_CALL:
        {"tool": "inspect_metrics", "args": {"threshold": 0.5}}

        Returns:
          dict: {tool_name: args_dict}
        """
        calls = {}
        for block in text.split("TOOL_CALL:"):
            block = block.strip()
            if not block:
                continue
            try:
                obj = json.loads(block)
                calls[obj["tool"]] = obj.get("args", {})
            except Exception:
                logger.warning(f"[Agent] [Parser] Failed to parse block: {block}")
        return calls

    # -----------------------------
    # One reasoning step (async)
    # -----------------------------
    async def _run_step(self, messages, step: int):
        logger.info(f"[Agent] [Step {step}] Calling LLM...")

        reply = await self.llm.async_chat(messages)
        logger.info(f"[Agent] [Step {step}] LLM replied: {reply[:200]}")

        calls = self._extract_tool_calls(reply)

        if not calls:
            logger.info(f"[Agent] [Step {step}] Final answer reached.")
            return reply, None

        logger.info(f"[Agent] [Step {step}] Tool calls: {list(calls.keys())}")

        # Run all tools concurrently
        tasks = {
            name: self.tools[name](**args)
            for name, args in calls.items()
        }

        tool_results = await gather_dict(tasks)
        logger.info(f"[Agent] [Step {step}] Tool results: {tool_results}")

        return reply, tool_results

    # -----------------------------
    # Full agent loop (async)
    # -----------------------------
    async def arun(self, run_summary: str):
        history = []
        messages = self._messages(run_summary, history)

        for step in range(1, self.max_steps + 1):
            reply, tool_results = await self._run_step(messages, step)

            if tool_results is None:
                return reply  # final answer

            # append tool outputs to chat
            history.append({
                "role": "tool",
                "content": json.dumps(tool_results, indent=2)
            })

            messages = self._messages(run_summary, history)

        logger.info("[Agent] [Final] Max steps reached, generating final answer")
        return await self.llm.async_chat(messages)

    # -----------------------------
    # Sync fallback wrapper
    # -----------------------------
    def run(self, run_summary: str):
        return asyncio.run(self.arun(run_summary))
