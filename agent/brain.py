
import json
import re
from typing import Literal

from google.genai import types
from pydantic import BaseModel

from config.gemini_client import generate_with_fallback


class AgentDecision(BaseModel):

    action: Literal["execute", "finish", "ask_user"]

    reasoning_summary: str

    message: str

    tool_name: str = ""

    # Store arguments as JSON text instead of dict
    tool_args: str = "{}"

    completion_summary: str = ""


def safe_json_loads(text: str):
    """
    Safely parse JSON and repair invalid backslash escapes
    commonly produced in AI-generated responses.
    """

    text = text.strip()

    # Remove Markdown JSON code fences if present
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        # Escape invalid backslashes without changing
        # valid JSON escape sequences.
        repaired_text = re.sub(
            r'\\(?!["\\/bfnrtu])',
            r"\\\\",
            text
        )

        return json.loads(repaired_text)


class AgentBrain:

    def __init__(self):
        pass

    def think(
        self,
        goal: str,
        plan: dict,
        history: list,
        available_tools: list
    ) -> AgentDecision:

        system_instruction = """
        You are the reasoning engine of an autonomous AI agent.

        Your responsibility is to achieve the user's goal
        through intelligent decisions.

        RULES:

        1. Understand the user's actual objective.
        2. Analyze the execution plan.
        3. Examine previous observations.
        4. Select the most appropriate available tool.
        5. Never invent tool names or parameters.
        6. Use only tools listed in available_tools.
        7. If a tool fails, consider another valid approach.
        8. Never claim an action succeeded without evidence.
        9. Choose finish ONLY when the user's success criteria
           are supported by actual observations.
        10. Do not finish merely because the plan was generated.
        11. If research is required, collect actual research results
            before writing the final report.
        12. If a required action has not been performed,
            continue executing available tools.
        13. If a tool fails, analyze the error and consider
            a different approach.
        14. If information is missing, choose ask_user.
        15. Otherwise, choose execute.
        16. Always use the actual tool parameters provided
            in the available_tools descriptions.
        17. When writing a report, use information collected
            from previous observations. Never fabricate research.

        For tool_args, return a valid JSON OBJECT
        encoded as a string.

        Example:
        {"query": "AI automation in businesses"}

        Use "{}" when no arguments are needed.

        The next decision must depend on the current context
        and previous observations.

        Do not follow a fixed execution sequence.

        Tool execution happens separately.
        You only recommend the next action.
        """

        # Prepare the agent's context
        context = {
            "user_goal": goal,
            "execution_plan": plan,
            "previous_observations": history,
            "available_tools": available_tools
        }

        # Ask Gemini to reason
        response = generate_with_fallback(
            contents=json.dumps(
                context,
                indent=2,
                default=str
            ),
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=AgentDecision,
                temperature=0.2
            )
        )

        # Check Gemini response
        if not response.text:
            raise ValueError(
                "Gemini returned an empty decision."
            )

        # Parse Gemini response safely
        try:
            response_data = safe_json_loads(response.text)

            decision = AgentDecision.model_validate(
                response_data
            )

        except Exception as error:
            raise ValueError(
                f"Failed to parse Gemini decision: {error}\n"
                f"Gemini response: {response.text}"
            ) from error

        # Validate tool selection
        if decision.action == "execute":

            valid_tools = {
                tool["name"]
                for tool in available_tools
            }

            if decision.tool_name not in valid_tools:
                raise ValueError(
                    f"Invalid tool selected: {decision.tool_name}"
                )

            # Validate JSON tool arguments
            try:
                parsed_args = safe_json_loads(
                    decision.tool_args
                )

            except Exception as error:
                raise ValueError(
                    f"Invalid tool arguments: {error}\n"
                    f"Tool args: {decision.tool_args}"
                ) from error

            if not isinstance(parsed_args, dict):
                raise ValueError(
                    "Tool arguments must be a JSON object."
                )

        return decision

