from typing import Any
from mcp.server.fastmcp import FastMCP
import logging
import random

# Initialize FastMCP server
mcp = FastMCP("ai_workshop")

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logging.debug("Logging system initialized.")

# Halloween costume database
HALLOWEEN_COSTUMES = {
    "classic": [
        "Vampire", "Witch", "Ghost", "Zombie", "Skeleton", "Frankenstein's Monster",
        "Mummy", "Werewolf", "Devil", "Angel", "Pirate", "Ninja"
    ],
    "pop_culture": [
        "Superhero (Batman, Superman, Spider-Man)", "Disney Character", "Star Wars Character",
        "Harry Potter Character", "Marvel Character", "Anime Character", "Video Game Character",
        "Movie Character", "TV Show Character", "Celebrity"
    ],
    "creative": [
        "Robot", "Alien", "Time Traveler", "Mad Scientist", "Steampunk Character",
        "Cyberpunk Character", "Fairy", "Elf", "Wizard", "Knight", "Princess",
        "Queen", "King", "Jester", "Clown", "Mime"
    ],
    "couples": [
        "Bonnie and Clyde", "Romeo and Juliet", "Batman and Catwoman",
        "Mario and Luigi", "Salt and Pepper", "Sun and Moon",
        "Day and Night", "Yin and Yang", "Thing 1 and Thing 2"
    ],
    "group": [
        "The Avengers", "The Justice League", "The Powerpuff Girls",
        "The Teenage Mutant Ninja Turtles", "The Spice Girls", "The Breakfast Club",
        "The Scooby-Doo Gang", "The Ghostbusters", "The X-Men"
    ],
    "scary": [
        "Pennywise the Clown", "Freddy Krueger", "Jason Voorhees", "Michael Myers",
        "Chucky", "Annabelle", "The Ring Girl", "The Grudge", "Leatherface",
        "Jigsaw", "Ghostface", "The Babadook"
    ],
    "cute": [
        "Pumpkin", "Black Cat", "Witch's Cat", "Broomstick", "Candy Corn",
        "Trick-or-Treater", "Baby Ghost", "Little Devil", "Fairy", "Butterfly",
        "Ladybug", "Bumblebee", "Unicorn", "Rainbow"
    ]
}

@mcp.tool()
async def suggest_halloween_costume(
    age: str = "adult",
    gender: str = "any", 
    style: str = "any",
    group_size: int = 1,
    scary_level: str = "medium"
) -> str:
    """
    Suggest Halloween costume ideas based on preferences.
    
    Args:
        age: Age group - "child", "teen", "adult", "senior"
        gender: Gender preference - "male", "female", "any"
        style: Costume style - "classic", "pop_culture", "creative", "scary", "cute", "any"
        group_size: Number of people (1 for individual, 2+ for group costumes)
        scary_level: Scare level - "low", "medium", "high"
    
    Returns:
        Halloween costume suggestion with details
    """
    logging.info(f"Halloween costume suggestion requested: age={age}, gender={gender}, style={style}, group_size={group_size}, scary_level={scary_level}")
    
    # Filter costumes based on preferences
    available_categories = []
    
    if style == "any":
        available_categories = list(HALLOWEEN_COSTUMES.keys())
    else:
        available_categories = [style]
    
    # Adjust for scary level
    if scary_level == "low":
        available_categories = [cat for cat in available_categories if cat not in ["scary"]]
    elif scary_level == "high":
        available_categories = ["scary"] if "scary" in available_categories else available_categories
    
    # Handle group costumes
    if group_size > 1:
        if "group" in available_categories:
            available_categories = ["group"]
        elif "couples" in available_categories and group_size == 2:
            available_categories = ["couples"]
    
    # Select random category and costume
    if not available_categories:
        available_categories = ["classic"]
    
    selected_category = random.choice(available_categories)
    selected_costume = random.choice(HALLOWEEN_COSTUMES[selected_category])
    
    # Generate suggestion with details
    suggestion = f"🎃 Halloween Costume Suggestion 🎃\n\n"
    suggestion += f"**Costume:** {selected_costume}\n"
    suggestion += f"**Category:** {selected_category.replace('_', ' ').title()}\n"
    suggestion += f"**Age Group:** {age.title()}\n"
    suggestion += f"**Scary Level:** {scary_level.title()}\n"
    
    if group_size > 1:
        suggestion += f"**Group Size:** {group_size} people\n"
    
    # Add costume tips based on category
    tips = {
        "classic": "Classic costumes are timeless and easy to find at costume stores!",
        "pop_culture": "Make sure to get the details right - accessories and makeup are key!",
        "creative": "This is your chance to be unique and creative with DIY elements!",
        "scary": "Focus on makeup and special effects to maximize the scare factor!",
        "cute": "Keep it adorable with bright colors and fun accessories!",
        "couples": "Coordinate your costumes for maximum impact!",
        "group": "Plan ahead to make sure everyone has their costume ready!"
    }
    
    if selected_category in tips:
        suggestion += f"\n**💡 Tip:** {tips[selected_category]}\n"
    
    # Add age-appropriate suggestions
    if age == "child":
        suggestion += "\n**Child-Friendly Note:** Make sure the costume is comfortable and safe for trick-or-treating!"
    elif age == "teen":
        suggestion += "\n**Teen Note:** This is a great age to experiment with makeup and special effects!"
    elif age == "adult":
        suggestion += "\n**Adult Note:** Consider comfort if you'll be wearing it for a long time!"
    
    logging.info(f"Suggested costume: {selected_costume} from category {selected_category}")
    
    return suggestion

if __name__ == "__main__":
    mcp.run(transport="stdio")
    logging.getLogger().handlers[0].flush()