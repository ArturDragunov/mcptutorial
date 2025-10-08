from mcp.server.fastmcp import FastMCP

# name of the mcp server
mcp=FastMCP("math")

@mcp.tool()
# add tool to the mcp server
def add(a:int,b:int)->int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a+b


@mcp.tool()
def multiply(a:int,b:int)->int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a*b

if __name__=="__main__":
    # stdio is the transport protocol for the mcp server. Alternatives could be streamable-http, http, websocket, etc.
    # use stdio for local development and for internet use http
    mcp.run(transport="stdio") 