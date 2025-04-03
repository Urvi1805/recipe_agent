import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="ChefGenius", page_icon="🍽️", layout="wide")

# Sidebar for user input
with st.sidebar:
    st.header("🍴 Recipe Input")
    ingredients = st.text_area("Ingredients (comma-separated)")
    dietary_restrictions = st.text_input("Dietary Restrictions (optional)")
    time_constraint = st.slider("Time Constraint (minutes)", min_value=5, max_value=120, value=45)
    get_recipe = st.button("🔍 Get Recipe")

# Main content area
st.markdown("""
    <style>
        .stApp {background-color: black;}
        .title {color: #FF6347; text-align: center; font-size: 3em;}
        .subtext {text-align: center; font-size: 1.2em; color: #DDD;}
        .result {background: #222; color: white; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(255,255,255,0.1);}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🍽️ ChefGenius Recipe Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Discover amazing recipes with the ingredients you have!</p>", unsafe_allow_html=True)

# Display recipe if button is clicked
if get_recipe:
    if ingredients:
        payload = {
            "ingredients": ingredients,
            "dietary_restrictions": dietary_restrictions,
            "time_constraint": time_constraint
        }
        
        response = requests.post("http://127.0.0.1:5001/get_recipe/", json=payload)
        
        if response.status_code == 200:
            recipe = response.json().get("recipe", "No recipe found.")
            st.markdown(f"<div class='result'>{recipe}</div>", unsafe_allow_html=True)
        else:
            st.error("Failed to fetch recipe. Please try again.")
    else:
        st.warning("Please enter at least one ingredient.")