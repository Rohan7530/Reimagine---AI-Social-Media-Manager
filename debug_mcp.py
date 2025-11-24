from server import mcp

tool = mcp.get_tool("post_to_twitter")
print(f"Tool object: {tool}")
print(f"Tool dir: {dir(tool)}")

if hasattr(tool, 'run'):
    print("Tool has 'run' method")
if hasattr(tool, 'fn'):
    print("Tool has 'fn' attribute")
    print(f"fn is callable? {callable(tool.fn)}")
