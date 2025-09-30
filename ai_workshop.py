from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging  # Add this import for logging
import os

# Initialize FastMCP server
mcp = FastMCP("ai_workshop")

# Constants
AI_WORKSHOP_BASE = "https://onelink.appsflyer.com/shortlink/v1"
USER_AGENT = "ai_workshop-app/1.0"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Content-Type": "application/json",
    "accept": "application/json",
    "authorization": os.environ.get('AF_ONELINK_TOKEN', '')  # Replace with your actual key or inject at runtime
}

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,              # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[logging.StreamHandler()]  # Output logs to stdout
)
logging.debug("Logging system initialized.")

async def call_ai_workshop(method: str, endpoint: str, params: dict[str, Any] = None, json: dict[str, Any] = None) -> Any:
    """Generic request handler for the AI Workshop API."""
    # Log the incoming parameters
    logging.info(f"Method: {method}, Endpoint: {endpoint}, Params: {params}, JSON: {json}")
    
    async with httpx.AsyncClient() as client:
        url = f"{AI_WORKSHOP_BASE}/{endpoint}"
        try:
            response = await client.request(method, url, headers=HEADERS, params=params, json=json, timeout=30.0)
            response.raise_for_status()
            if method.upper() == "GET":
                return response.json()
            else:
                return response.text
        except httpx.HTTPStatusError as e:
            return f"Error {e.response.status_code}: {e.response.text}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

@mcp.tool()
async def create_ai_workshop(ai_workshop_id: str, data: dict[str, Any], brand_domain: str = None, ttl: str = None, shortlink_id: str = None) -> str:
    """Create an AI Workshop attribution link."""
    # Log the incoming parameters
    logging.info(f"create_ai_workshop called with ai_workshop_id: {ai_workshop_id}, data: {data}, brand_domain: {brand_domain}, ttl: {ttl}, shortlink_id: {shortlink_id}")
    
    payload = {
        "data": data
    }
    if brand_domain:
        payload["brand_domain"] = brand_domain
    if ttl:
        payload["ttl"] = ttl
    params = {"id": shortlink_id} if shortlink_id else {}
    return await call_ai_workshop("POST", ai_workshop_id, params=params, json=payload)

@mcp.tool()
async def get_ai_workshop(ai_workshop_id: str, shortlink_id: str) -> str:
    """Get details of an AI Workshop."""
    # Log the incoming parameters
    logging.info(f"get_ai_workshop called with ai_workshop_id: {ai_workshop_id}, shortlink_id: {shortlink_id}")
    
    params = {"id": shortlink_id}
    return await call_ai_workshop("GET", ai_workshop_id, params=params)

@mcp.tool()
async def update_ai_workshop(ai_workshop_id: str, shortlink_id: str, data: dict[str, Any], brand_domain: str = None, ttl: str = None) -> str:
    """Update an AI Workshop attribution link."""
    # Log the incoming parameters
    logging.info(f"update_ai_workshop called with ai_workshop_id: {ai_workshop_id}, shortlink_id: {shortlink_id}, data: {data}, brand_domain: {brand_domain}, ttl: {ttl}")
    
    payload = {
        "data": data
    }
    if brand_domain:
        payload["brand_domain"] = brand_domain
    if ttl:
        payload["ttl"] = ttl
    params = {"id": shortlink_id}
    return await call_ai_workshop("PUT", ai_workshop_id, params=params, json=payload)

@mcp.tool()
async def delete_ai_workshop(ai_workshop_id: str, shortlink_id: str) -> str:
    """Delete an AI Workshop attribution link."""
    # Log the incoming parameters
    logging.info(f"delete_ai_workshop called with ai_workshop_id: {ai_workshop_id}, shortlink_id: {shortlink_id}")
    
    params = {"id": shortlink_id}
    return await call_ai_workshop("DELETE", ai_workshop_id, params=params)

if __name__ == "__main__":
    mcp.run(transport="stdio")
    logging.getLogger().handlers[0].flush()