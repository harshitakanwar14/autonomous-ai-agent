
from tools.calculator import calculate
from tools.web_search import search_web
from tools.file_reader import read_file
from tools.file_writer import write_file


class ToolRegistry:

    def __init__(self):
        self.tools = {}

        # Register all available tools
        self.register(
            "calculator",
            "Performs mathematical calculations.",
            calculate,
            {"expression": "Mathematical expression"}
        )

        self.register(
            "web_search",
            "Searches the internet for relevant information.",
            search_web,
            {
                "query": "Search query",
                "max_results": "Optional number of results"
            }
        )

        self.register(
            "file_reader",
            "Reads text, Markdown, CSV, JSON and log files.",
            read_file,
            {"path": "Relative file path inside project"}
        )

        self.register(
            "file_writer",
            "Creates files inside the output directory.",
            write_file,
            {
                "filename": "Output filename",
                "content": "Content to save"
            }
        )

    def register(
        self,
        name,
        description,
        function,
        parameters
    ):

        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }

    def get_available_tools(self):

        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for tool in self.tools.values()
        ]

    def execute(self, name, arguments):

        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a dictionary.")

        tool = self.tools[name]

        # Execute the selected Python function
        result = tool["function"](**arguments)

        return {
            "success": True,
            "tool": name,
            "result": result
        }
