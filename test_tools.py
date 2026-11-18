
from tools.registry import ToolRegistry


def test_tools():

    registry = ToolRegistry()

    print("\nAVAILABLE TOOLS:")

    for tool in registry.get_available_tools():
        print("-", tool["name"])

    # Test 1: Calculator
    print("\nTEST 1: CALCULATOR")

    result = registry.execute(
        "calculator",
        {"expression": "25 * 4 + 100"}
    )

    print(result)

    # Test 2: File Writer
    print("\nTEST 2: FILE WRITER")

    result = registry.execute(
        "file_writer",
        {
            "filename": "test_report.md",
            "content": "# Test Report\n\nTool execution works!"
        }
    )

    print(result)

    # Test 3: File Reader
    print("\nTEST 3: FILE READER")

    result = registry.execute(
        "file_reader",
        {"path": "output/test_report.md"}
    )

    print(result)

    # Test 4: Web Search
    print("\nTEST 4: WEB SEARCH")

    result = registry.execute(
        "web_search",
        {
            "query": "Applications of AI automation in businesses",
            "max_results": 3
        }
    )

    print(result)


if __name__ == "__main__":
    test_tools()
