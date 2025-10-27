from mcp.server.fastmcp import FastMCP
import logging

# Initialize FastMCP server
mcp = FastMCP("halloween_workshop")

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")