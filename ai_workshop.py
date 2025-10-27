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

@mcp.tool()
async def suggest_halloween_costume() -> str:
    """
    Suggest a random Halloween costume idea.
    
    This tool provides a simple Halloween costume suggestion without any parameters.
    Perfect for getting quick inspiration for your Halloween costume!
    
    Returns:
        A Halloween costume suggestion with details
    """
    costumes = [
        "🎃 Vampire - Classic and elegant with fangs and cape",
        "🧙‍♀️ Witch - Traditional with pointy hat and broomstick", 
        "👻 Ghost - Simple white sheet with eye holes",
        "🧟‍♂️ Zombie - Tattered clothes and zombie makeup",
        "💀 Skeleton - Black outfit with bone patterns",
        "🤖 Robot - Silver outfit with metallic accessories",
        "🦸‍♀️ Superhero - Cape, mask, and heroic pose",
        "🎭 Pirate - Eye patch, hat, and treasure map",
        "🐱 Black Cat - Black outfit with cat ears and tail",
        "🎪 Clown - Colorful outfit with face paint"
    ]
    
    import random
    selected_costume = random.choice(costumes)
    
    return f"🎃 Halloween Costume Suggestion 🎃\n\n{selected_costume}\n\nHappy Halloween! 👻"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")