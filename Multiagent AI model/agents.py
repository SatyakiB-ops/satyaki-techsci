from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

import os
from dotenv import load_dotenv

load_dotenv()

# Basic sanity check on required API keys so failures are clear immediately,
# instead of a confusing TypeError later.
required_keys = ["OPENAI_API_KEY", "GROQ_API_KEY", "TAVILY_API_KEY"]
missing = [k for k in required_keys if not os.getenv(k)]
if missing:
    raise EnvironmentError(
        f"Missing required environment variable(s): {', '.join(missing)}. "
        f"Add them to your .env file in this folder."
    )

# ============================================================================
# Agent 1: Destination Research Agent
# ============================================================================
destination_research_agent = Agent(
    name="Destination Research Agent",
    role="Find attractions, activities, events, and things to do at travel destinations",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TavilyTools()],
    instructions=[
        "Search for top attractions, museums, parks, and landmarks",
        "Find local events, festivals, and cultural activities happening during the travel dates",
        "Include opening hours, entry fees, and visitor ratings when available",
        "Provide hidden gems and lesser-known attractions",
        "Always include sources for all information",
        "Format recommendations as a structured list",
    ],
    markdown=True,
)

# ============================================================================
# Agent 2: Budget Optimizer Agent
# ============================================================================
budget_optimizer_agent = Agent(
    name="Budget Optimizer Agent",
    role="Find and compare flights, hotels, transportation deals, and calculate trip costs",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TavilyTools()],
    instructions=[
        "Search for flight deals and airlines for the specified dates and locations",
        "Find affordable hotel options with different price ranges (budget, mid-range, luxury)",
        "Look for car rental, public transportation, and local travel options with costs",
        "Calculate total estimated costs for the trip",
        "Provide budget breakdown (flights, accommodation, food, activities)",
        "Include booking tips and money-saving recommendations",
        "Always present information in tables for easy comparison",
        "Include currency information and conversion tips for international travel",
    ],
    markdown=True,
)

# ============================================================================
# Agent 3: Weather & Climate Agent
# ============================================================================
weather_climate_agent = Agent(
    name="Weather & Climate Agent",
    role="Check weather forecasts, best travel seasons, and climate conditions",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TavilyTools()],
    instructions=[
        "Search for current weather conditions and forecasts for the destination",
        "Provide information about the best season to visit (weather-wise)",
        "Include average temperatures, rainfall, humidity for the travel dates",
        "Suggest appropriate clothing and packing recommendations",
        "Warn about typhoon seasons, monsoons, extreme weather conditions",
        "Provide humidity and UV index information when relevant",
        "Include tips for dealing with weather challenges",
        "Always cite weather sources",
    ],
    markdown=True,
)

# ============================================================================
# Agent 4: Local Guide Agent
# ============================================================================
local_guide_agent = Agent(
    name="Local Guide Agent",
    role="Find restaurants, safety tips, local customs, transportation, and cultural insights",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TavilyTools()],
    instructions=[
        "Search for popular local restaurants, street food, and dining recommendations",
        "Provide safety information, travel warnings, and precautions",
        "Include local customs, etiquette, and cultural tips to respect local traditions",
        "Find local transportation options (metro, buses, taxis, rickshaws)",
        "Include emergency contacts and important phone numbers",
        "Provide visa requirements and travel documentation needed",
        "Include language tips and useful local phrases",
        "Always include sources for safety and travel warnings",
    ],
    markdown=True,
)

# ============================================================================
# Master Travel Coordinator Team
# ============================================================================
travel_coordinator = Team(
    name="Travel Trip Planner",
    members=[
        destination_research_agent,
        budget_optimizer_agent,
        weather_climate_agent,
        local_guide_agent,
    ],
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "Coordinate all four agents to gather complete travel information",
        "Create a comprehensive day-by-day itinerary",
        "Include attractions, meals, activities, and rest times for each day",
        "Provide complete cost breakdown with budget estimates",
        "Include weather updates and appropriate clothing recommendations",
        "Add local safety tips, cultural notes, and important contacts",
        "Use tables to display flights, hotels, costs, and schedules",
        "Provide a packing checklist based on weather and activities",
        "Include booking recommendations and important travel tips",
        "Organize information in a clear, actionable format",
        "Always include sources for all recommendations",
    ],
    markdown=True,
)

# ============================================================================
# Main Execution
# ============================================================================
if __name__ == "__main__":
    query = """
    Plan a 20-day trip to Switzerland starting December 1, 2026, ending December 20, 2026.
    Budget: $5,000 per person (including flights from Kolkata)
    Interests: Technology, culture, food, temples, modern attractions
    Travel group: 2 adults

    Please provide:
    1. Day-by-day detailed itinerary with attractions and timings
    2. Complete flight and hotel recommendations with costs
    3. Weather forecast and packing recommendations
    4. Restaurant recommendations for different cuisines
    5. Local tips, safety information, and cultural customs
    6. Transportation options and estimated costs
    7. Budget breakdown and money-saving tips
    8. Booking recommendations and travel warnings
    """

    print("=" * 80)
    print("TRAVEL TRIP PLANNER - COMPREHENSIVE ITINERARY")
    print("=" * 80)

    travel_coordinator.print_response(query, stream=True)