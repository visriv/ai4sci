import json
from pathlib import Path
from .llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger("Agent")

class RCAAgent:
    def __init__(self, llm_model, system_prompt_path, tools: dict, max_steps=4):
        self.llm = LLMClient(llm_model, host="http://127.0.0.1:11434")
        self.tools = tools
        self.max_steps = max_steps

        self.system_prompt = Path(system_prompt_path).read_text().strip()

        logger.info("[Agent] [Init] RCA Agent initialized")

    def _messages(self, run_summary: str):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": run_summary},
        ]

    def run(self, run_summary: str):
        messages = self._messages(run_summary)

        for step in range(1, self.max_steps + 1):

            logger.info(f"[Agent] [Step {step}] Sending messages to LLM...")

            reply = self.llm.chat(messages)
            logger.info(f"[Agent] [Step {step}] LLM replied: {reply[:200]}")

            # Detect tool call
            if reply.startswith("TOOL_CALL:"):
                try:
                    payload = json.loads(reply.replace("TOOL_CALL:", "", 1))
                    tool_name = payload["tool"]
                    args = payload.get("args", {})

                    logger.info(f"[Agent] [Step {step}] Tool call requested: {tool_name} args={args}")

                    if tool_name not in self.tools:
                        logger.error(f"[Agent] Unknown tool '{tool_name}'")
                        break

                    tool_output = self.tools[tool_name](**args)

                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_output, indent=2)
                    })
                except Exception as e:
                    logger.error(f"[Agent] Tool call parse error: {e}")
                    break

            else:
                logger.info(f"[Agent] [Step {step}] Final diagnosis returned.")
                return reply

        logger.info("[Agent] [Final] Generating fallback answer")
        return self.llm.chat(messages)
