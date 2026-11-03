from fastmcp import FastMCP

mcp = FastMCP("Calculator MCP Server")

@mcp.tool()
def add(a,b):
    """Add two numbers
    arguments:
        a (int or float): The first number
        b (int or float): The second number
    returns:
        int or float: The sum of a and b
    """
    return a + b

@mcp.tool()
def subtract(a,b):
    """Subtract two numbers
    arguments:
        a (int or float): The first number
        b (int or float): The second number
    returns:
        int or float: The difference of a and b
    """
    return a - b

@mcp.tool()
def multiply(a,b):
    """Multiply two numbers
    arguments:
        a (int or float): The first number
        b (int or float): The second number
    returns:
        int or float: The product of a and b
    """
    return a * b

@mcp.tool()
def divide(a,b):
    """Divide two numbers
    arguments:
        a (int or float): The first number
        b (int or float): The second number
    returns:
        int or float: The quotient of a and b
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8085)