
import json
from datetime import datetime, timezone


class AgentObserver:

    def observe(
        self,
        iteration,
        decision,
        execution_result
    ):

        # Capture the actual execution result
        observation = {
            "iteration": iteration,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "reasoning": decision.reasoning_summary,

            "action": decision.action,

            "tool": execution_result.get("tool"),

            "success": execution_result.get("success"),

            "result": execution_result.get("result"),

            "error": execution_result.get("error")
        }

        # Keep observations within a manageable size
        serialized = json.dumps(
            observation,
            default=str
        )

        if len(serialized) > 12000:
            observation["result"] = (
                serialized[:11500]
                + "... [Output truncated]"
            )

        return observation
