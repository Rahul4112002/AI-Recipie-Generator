from flask import Flask, render_template, request
from markupsafe import Markup
import google.generativeai as genai

app = Flask(__name__)

# Your API key (make sure to keep this secure)
API_KEY = "AIzaSyDvNcXTExEzcRnQa5ziZxXALsgCF1VeAZ0"

def format_recipe_text(recipe_text):
    # Replace Markdown-like syntax with HTML tags
    recipe_text = recipe_text.replace('**', '<strong>').replace('*', '</strong>')
    return recipe_text

def generate_recipe(ingredients):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Generate the recipe using the following ingredients: {', '.join(ingredients)}"
    response = model.generate_content(prompt)
    
    formatted_recipe = format_recipe_text(response.text)
    return Markup(formatted_recipe)

@app.route('/', methods=['GET', 'POST'])
def index():
    recipe = None
    if request.method == 'POST':
        user_input = request.form['ingredients']
        ingredients = (ingredient.strip() for ingredient in user_input.split(','))
        recipe = generate_recipe(ingredients)
    return render_template('index.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
