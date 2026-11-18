import json

from agent.planner import AgentPlanner
from agent.brain import AgentBrain
from agent.executor import AgentExecutor
from agent.observer import AgentObserver
from agent.memory import AgentMemory

from tools.registry import ToolRegistry

from config.settings import MAX_ITERATIONS


def print_section(title):

    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)


def run_agent():

    print_section("AUTONOMOUS AI AGENT")

    goal = input("\nEnter your objective: ").strip()

    if not goal:
        print("Please enter a valid objective.")
        return

    registry = ToolRegistry()

    available_tools = registry.get_available_tools()

    planner = AgentPlanner()
    brain = AgentBrain()
    executor = AgentExecutor(registry)
    observer = AgentObserver()
    memory = AgentMemory()

    run_id = None

    try:

        # STEP 1: Generate a dynamic execution plan
        print_section("STEP 1: PLANNING")

        plan = planner.create_plan(
            goal=goal,
            available_tools=available_tools
        )

        print(plan.model_dump_json(indent=2))

        # STEP 2: Start persistent memory
        run_id = memory.start_run(
            goal,
            plan.model_dump()
        )

        print("\nExecution ID:", run_id)

        history = []

        # STEP 3: Autonomous execution loop
        print_section("STEP 2: AUTONOMOUS EXECUTION")

        for iteration in range(1, MAX_ITERATIONS + 1):

            print(f"\nITERATION {iteration}/{MAX_ITERATIONS}")

            # Brain reasons about the next action
            print("\n[AGENT BRAIN] Thinking...")

            decision = brain.think(
                goal=goal,
                plan=plan.model_dump(),
                history=history[-10:],
                available_tools=available_tools
            )

            print("\nDECISION:")
            print(decision.model_dump_json(indent=2))

            # Check if task is complete
            if decision.action == "finish":

                print_section("TASK COMPLETED")

                print(
                    decision.completion_summary
                    or decision.message
                )

                memory.update_status(
                    run_id,
                    "completed"
                )

                return

            # Check if user input is required
            if decision.action == "ask_user":

                print_section("USER INPUT REQUIRED")

                print(decision.message)

                memory.update_status(
                    run_id,
                    "paused"
                )

                return

            # Execute selected tool
            print("\n[EXECUTOR] Executing tool...")

            execution_result = executor.execute(decision)

            print("\nTOOL RESULT:")

            print(
                json.dumps(
                    execution_result,
                    indent=2,
                    default=str
                )[:12000]
            )

            # Observe the result
            observation = observer.observe(
                iteration,
                decision,
                execution_result
            )

            # Save observation in persistent memory
            memory.add_observation(
                run_id,
                iteration,
                observation
            )

            # Update history for the next Brain decision
            history.append(observation)

            print("\n[OBSERVER] Observation saved.")

            if not execution_result["success"]:
                print(
                    "[OBSERVER] Tool execution failed. "
                    "Brain will receive the error."
                )

        # STEP 4: Maximum iteration protection
        print_section("EXECUTION LIMIT REACHED")

        memory.update_status(
            run_id,
            "max_iterations"
        )

        print(
            "The agent reached its maximum iteration limit "
            "before confirming task completion."
        )

    except Exception as error:

        print_section("AGENT ERROR")

        print(str(error))

        if run_id:
            memory.update_status(
                run_id,
                "failed"
            )


if __name__ == "__main__":
    run_agent()
