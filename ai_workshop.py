from mcp.server.fastmcp import FastMCP
import logging
from typing import Literal

# Initialize FastMCP server
mcp = FastMCP("halloween_workshop")

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

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
    age: Literal["child", "teen", "adult", "senior"] = "adult",
    gender: Literal["male", "female", "any"] = "any", 
    style: Literal["classic", "pop_culture", "creative", "scary", "cute", "any"] = "any",
    group_size: int = 1,
    scary_level: Literal["low", "medium", "high"] = "medium"
) -> str:
    """
    Suggest Halloween costume ideas based on preferences.
    
    Args:
        age: Age group - child, teen, adult, or senior
        gender: Gender preference - male, female, or any
        style: Costume style - classic, pop_culture, creative, scary, cute, or any
        group_size: Number of people (1 for individual, 2+ for group costumes)
        scary_level: Scare level - low, medium, or high
    
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
    
    import random
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

@mcp.resource("halloween://costume-inventory")
async def costume_inventory() -> str:
    """
    Halloween costume inventory resource.
    
    This resource provides access to the complete Halloween costume database,
    organized by categories. Perfect for browsing all available costume options
    or understanding the full range of choices available.
    
    Returns:
        Complete Halloween costume inventory organized by categories
    """
    inventory = "# 🎃 Halloween Costume Inventory 🎃\n\n"
    inventory += "Browse our complete collection of Halloween costumes organized by category:\n\n"
    
    for category, costumes in HALLOWEEN_COSTUMES.items():
        inventory += f"## {category.replace('_', ' ').title()} Costumes\n\n"
        
        # Group costumes for better readability
        for i, costume in enumerate(costumes, 1):
            inventory += f"{i}. {costume}\n"
        
        inventory += "\n"
    
    inventory += "---\n\n"
    inventory += "**Total Costumes Available:** " + str(sum(len(costumes) for costumes in HALLOWEEN_COSTUMES.values())) + "\n"
    inventory += "**Categories:** " + str(len(HALLOWEEN_COSTUMES)) + "\n\n"
    inventory += "Use the `suggest_halloween_costume` tool to get personalized recommendations based on your preferences! 👻"
    
    return inventory

@mcp.prompt()
def halloween_costume_prompts() -> str:
    """
    Get interactive prompts to help choose the perfect Halloween costume.
    
    This prompt provides a series of questions and prompts to guide users through
    the costume selection process. Perfect for those who need help deciding
    what to be for Halloween!
    
    Returns:
        Interactive prompts and questions for costume selection
    """
    prompts = """
# 🎃 Halloween Costume Selection Prompts 🎃

Let's find your perfect Halloween costume! Answer these questions to get personalized suggestions:

## 1. Age & Comfort Level
- Are you dressing up as a child, teen, adult, or senior?
- Do you prefer comfortable costumes or are you okay with elaborate ones?
- Will you be walking around a lot (trick-or-treating, parties)?

## 2. Style Preferences
- **Classic**: Traditional Halloween costumes (vampire, witch, ghost)
- **Pop Culture**: Characters from movies, TV, games, books
- **Creative**: Unique, DIY, or artistic costumes
- **Scary**: Horror movie characters and frightening costumes
- **Cute**: Adorable, fun, and family-friendly costumes

## 3. Group or Solo?
- Are you dressing up alone or with others?
- If with others: couples costume or group theme?
- Do you want to coordinate with friends/family?

## 4. Scare Factor
- **Low**: Family-friendly, not scary at all
- **Medium**: Somewhat spooky but not terrifying
- **High**: Maximum scare factor for adults only

## 5. Budget & Time
- How much time do you have to prepare?
- What's your budget range?
- Do you prefer store-bought or DIY costumes?

## 6. Special Considerations
- Any allergies to makeup or materials?
- Will you be indoors or outdoors?
- Do you need to eat/drink while wearing the costume?

---

**Next Steps:**
1. Answer these questions for yourself
2. Use the `suggest_halloween_costume` tool with your preferences
3. Browse the costume inventory resource for more options
4. Get creative and have fun! 👻

**Pro Tip:** Don't be afraid to mix and match ideas or put your own spin on classic costumes!
"""
    
    return prompts

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")