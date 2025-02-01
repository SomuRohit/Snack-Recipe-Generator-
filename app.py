from flask import Flask, render_template, request, jsonify
import random
import json
from urllib.request import urlopen, quote
import urllib.error

app = Flask(__name__)

snacks = [
    {"name": "Paneer Tikka Sandwich", "ingredients": ["Paneer", "Bread", "Onion", "Capsicum", "Spices", "Yogurt"], "instructions": "Marinate paneer, grill/pan-fry, and assemble in a sandwich with veggies."},
    {"name": "Tofu Scramble Sandwich", "ingredients": ["Tofu", "Bread", "Onion", "Tomato", "Spices"], "instructions": "Scramble tofu with spices, and use as filling in a sandwich."},
    {"name": "Besan Chilla", "ingredients": ["Besan (Gram Flour)", "Onion", "Tomato", "Spices", "Green Chilies"], "instructions": "Mix besan with spices and veggies, make a batter, and pan-fry like a pancake."},
    {"name": "Moong Dal Cheela", "ingredients": ["Moong Dal (Split Yellow Lentils)", "Ginger", "Green Chilies", "Spices"], "instructions": "Soak and grind moong dal, add spices, and pan-fry like a thin pancake."},
    {"name": "Sprouts Salad", "ingredients": ["Mixed Sprouts", "Onion", "Tomato", "Cucumber", "Lemon Juice", "Spices"], "instructions": "Combine sprouts with chopped veggies and spices. Add lemon juice."},
    {"name": "Peanut Masala Sandwich", "ingredients": ["Boiled Peanuts", "Onion", "Tomato", "Green Chilies", "Lemon Juice", "Spices", "Bread"], "instructions": "Mix peanuts with spices and veggies, and use as a sandwich filling."},
    {"name": "Egg Bhurji Sandwich", "ingredients": ["Eggs", "Onion", "Tomato", "Green Chilies", "Spices", "Bread"], "instructions": "Scramble eggs with spices and veggies, and use as a sandwich filling."},
    {"name": "Masala Omelette", "ingredients": ["Eggs", "Onion", "Tomato", "Green Chilies", "Spices"], "instructions": "Whisk eggs with spices and veggies, and cook like an omelette."},
    {"name": "Aloo Tikki", "ingredients": ["Potatoes", "Peas", "Spices", "Breadcrumbs"], "instructions": "Boil and mash potatoes, mix with peas and spices, form tikkis, and shallow fry."},
    {"name": "Soya Chunk Fry", "ingredients": ["Soya Chunks", "Onion", "Tomato", "Spices", "Yogurt"], "instructions": "Soak soya chunks, marinate with spices and yogurt, and pan-fry until crispy."},
    {"name": "Mushroom and Corn Sandwich", "ingredients": ["Mushrooms", "Corn", "Onion", "Garlic", "Spices", "Bread"], "instructions": "Saute mushrooms, corn, onion, and garlic with spices. Use as a sandwich filling."},
    {"name": "Vegetable Cutlet", "ingredients": ["Mixed Vegetables", "Potatoes", "Spices", "Breadcrumbs"], "instructions": "Boil and mash vegetables, mix with potatoes and spices, form cutlets, and shallow fry."},
    {"name": "Rava Dosa", "ingredients": ["Rava (Semolina)", "Rice Flour", "Onion", "Green Chilies", "Spices"], "instructions": "Mix rava, rice flour, and spices with water. Make thin dosas on a hot griddle."},
    {"name": "Poha", "ingredients": ["Flattened Rice (Poha)", "Onion", "Potatoes", "Peanuts", "Spices"], "instructions": "Soak poha, saute with spices and other ingredients."},
    {"name": "Upma", "ingredients": ["Semolina (Sooji/Rava)", "Onion", "Vegetables", "Spices"], "instructions": "Roast semolina, then cook with spices and vegetables."},
    {"name": "Idli", "ingredients": ["Rice", "Urad Dal (Split Black Gram)"], "instructions": "Soak and grind rice and urad dal, ferment, and steam to make idlis."},
    {"name": "Dhokla", "ingredients": ["Fermented Batter (Besan, Rice)", "Eno Fruit Salt", "Spices"], "instructions": "Steam the fermented batter with eno and spices."},
    {"name": "Khakhra", "ingredients": ["Whole Wheat Flour", "Spices"], "instructions": "Make thin crispy flatbreads by roasting on a griddle."}
]

# Fruity Milkshakes (Indian Flavors)
shakes = [
    {"name": "Mango Lassi", "ingredients": ["Mango", "Yogurt", "Milk", "Cardamom", "Sugar/Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Banana Cardamom Shake", "ingredients": ["Banana", "Milk", "Cardamom", "Sugar/Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Strawberry Rose Lassi", "ingredients": ["Strawberries", "Yogurt", "Milk", "Rose Syrup", "Sugar/Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Chikoo (Sapota) Shake", "ingredients": ["Chikoo", "Milk", "Sugar/Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Muskmelon Mint Cooler", "ingredients": ["Muskmelon", "Mint Leaves", "Yogurt", "Milk", "Sugar/Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Pineapple Ginger Smoothie", "ingredients": ["Pineapple", "Ginger", "Yogurt", "Milk", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Watermelon Mint Refresher", "ingredients": ["Watermelon", "Mint Leaves", "Lime Juice", "Sugar"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Guava Chili Shake", "ingredients": ["Guava", "Green Chili", "Ginger", "Milk", "Sugar/Jaggery"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Pomegranate Smoothie", "ingredients": ["Pomegranate Arils", "Yogurt", "Milk", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Apple Cinnamon Shake", "ingredients": ["Apple", "Milk", "Cinnamon", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Papaya Orange Smoothie", "ingredients": ["Papaya", "Orange Juice", "Yogurt", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Avocado Milkshake", "ingredients": ["Avocado", "Milk", "Honey", "Cardamom"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Dates and Nuts Shake", "ingredients": ["Dates", "Almonds", "Cashews", "Milk", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Fig and Honey Shake", "ingredients": ["Figs", "Milk", "Honey"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Saffron Pistachio Lassi", "ingredients": ["Yogurt", "Milk", "Saffron", "Pistachios", "Sugar"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Rose and Almond Milkshake", "ingredients": ["Milk", "Rose Syrup", "Almonds", "Sugar"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Cardamom and Pistachio Shake", "ingredients": ["Milk", "Cardamom Powder", "Pistachios", "Sugar"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Chocolate and Banana Shake", "ingredients": ["Banana", "Milk", "Cocoa Powder", "Chocolate Syrup"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Vanilla and Berry Shake", "ingredients": ["Milk", "Vanilla Ice Cream", "Mixed Berries"], "instructions": "Blend all ingredients until smooth."},
    {"name": "Coffee and Walnut Shake", "ingredients": ["Coffee", "Milk", "Walnuts", "Sugar"], "instructions": "Blend all ingredients until smooth."}
]
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/recipe", methods=["GET"])
def recipe_api():
    ingredient = request.args.get("ingredient", "").strip()
    if not ingredient:
        return jsonify({"error": "Please enter an ingredient"}), 400

    recipes = get_recipe(ingredient)
    if not recipes:
        return jsonify({"error": "No recipes found"}), 404

    try:  
        selected_recipe = recipes[0]['recipe']
        recipe_data = {
            "label": selected_recipe.get("label", "No title"),
            "ingredientLines": selected_recipe.get("ingredientLines", []),
            "url": selected_recipe.get("url", "")
        }
        return jsonify(recipe_data)
    except (IndexError, KeyError, TypeError):  # Handle potential data errors
        return jsonify({"error": "Error processing recipe data"}), 500


@app.route("/api/random_snack", methods=["GET"])
def random_snack():
    snack = random.choice(snacks)
    return jsonify({
        "label": snack["name"],
        "ingredientLines": snack["ingredients"],
        "url": None,
        "instructions": snack["instructions"]
    })

@app.route("/api/random_shake", methods=["GET"])
def random_shake():
    shake = random.choice(shakes)
    return jsonify({
        "label": shake["name"],
        "ingredientLines": shake["ingredients"],
        "url": None,
        "instructions": shake["instructions"]
    })

def get_recipe(ingredient):
    api_key = '7a7cd9b85dd6e0d516903b7c2d582bfa'  
    application_id = 'a720f909'  

    encoded_ingredient = quote(ingredient, safe='')
    url = f'https://api.edamam.com/search?app_id={application_id}&app_key={api_key}&q={encoded_ingredient}'

    try:
        with urlopen(url) as response:
            data = json.load(response)
            return data.get('hits', [])
    except urllib.error.URLError as e:
        print(f"Error fetching data from API: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return []

if __name__ == "__main__":
    app.run(debug=True)