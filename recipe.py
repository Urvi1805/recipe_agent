from fastapi import FastAPI
from pydantic import BaseModel
from textwrap import dedent
from agno.agent import Agent,RunResponse
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


recipe_agent = Agent(
    name="ChefGenius",
    tools=[DuckDuckGoTools()],
    model=Groq(id="qwen-2.5-32b"),
    description=dedent("""
        You are ChefGenius, a passionate and knowledgeable culinary expert with expertise in global cuisine! 🍳
        Your mission is to help users create delicious meals by providing detailed,
        personalized recipes based on their available ingredients, dietary restrictions,
        and time constraints.
    """),
    instructions=dedent("""
        Approach each recipe recommendation mainly focused on indian dishes domain with structured analysis, recipe selection, detailed information, 
        give proper indian dishe name which actually exist for that use web to give more accurate results.
        and extra features such as ingredient substitutions but consider all ingrediants in the main recipe, plating suggestions, and dietary accommodations and also tell extras that requires to eat like (Roti,Naan,Paratha,Papad,Pickle etc...).
        - give in proper markdown format and start from recipe name and then other details it should be in proper structured format.
        - separate each part in different points.                
                        """),
    markdown=True,
    add_datetime_to_instructions=True,
    # show_tool_calls=True,
)

class RecipeRequest(BaseModel):
    ingredients: str
    dietary_restrictions: str = ""
    time_constraint: int = 45  
    

@app.post("/get_recipe/")
def get_recipe(request: RecipeRequest):
    query = f"I have {request.ingredients}. Need a recipe with dietary restrictions: {request.dietary_restrictions}, taking less than {request.time_constraint} minutes."
    
    response: RunResponse = recipe_agent.run(query)
    return {"recipe": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('recipe:app',host='127.0.0.1',port=5001,reload=True)