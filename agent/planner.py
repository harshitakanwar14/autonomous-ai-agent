
import json

from google.genai import types
from pydantic import BaseModel, Field

from config.gemini_client import generate_with_fallback


class PlanStep(BaseModel):
    step_id: int
    task: str
    expected_result: str
    suggested_tool: str


class ExecutionPlan(BaseModel):
    objective: str
    approach: str
    steps: list[PlanStep] = Field(min_length=1, max_length=10)
    success_criteria: list[str]


class AgentPlanner:

    def __init__(self):
        pass

    def create_plan(
        self,
        goal: str,
        available_tools: list = None
    ) -> ExecutionPlan:

        if not goal or not goal.strip():
            raise ValueError("Objective cannot be empty.")

        available_tools = available_tools or []

        system_instruction = """
        You are an intelligent planning engine.

        Your job is to create a dynamic execution plan
        for the user's objective.

        Instructions:

        1. Understand the user's objective.
        2. Break it into meaningful tasks.
        3. Arrange tasks in logical order.
        4. Explain the expected result of each task.
        5. Suggest appropriate available tools.
        6. Do not assume any task has been completed.
        7. Avoid unnecessary steps.
        8. Generate plans according to the actual objective.
        9. Never invent unavailable tools.

        Return a structured execution plan.
        """

        # IMPORTANT: Create context before using it
        context = {
            "user_objective": goal,
            "available_tools": available_tools
        }

        # Ask Gemini to generate the plan
        response = generate_with_fallback(
            contents=json.dumps(context, indent=2),
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ExecutionPlan,
                temperature=0.3
            )
        )

        if not response.text:
            raise ValueError("Gemini returned an empty plan.")

        # Validate Gemini's response
        plan = ExecutionPlan.model_validate_json(
            response.text
        )

        # Correct step numbering
        for index, step in enumerate(
            plan.steps,
            start=1
        ):
            step.step_id = index

        return plan
