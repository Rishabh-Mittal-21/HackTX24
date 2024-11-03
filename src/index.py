from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import secrets
import os
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from openai import OpenAI

client = OpenAI("KEY")

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    resturant = StringField('Restaurant?', validators=[DataRequired(), Length(10, 40)])
    item = StringField('Item?', validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField('Submit')

def getIngredients(item):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are given a fast food menu item. \
                Break down the ingredients at a high level and provide the price \
                each item would cost at a grocery store. Stick to very general \
                foods needed, keeping answers for the ingredients to a 2-word \
                maximum. Use basic versions of how the food would be made. Ensure \
                the ingredients and prices are all comma-separated. \
                All entries must have a valu and ingredient. An example \
                entry would be: ingredient1, price1, ingredient2, price2, ... \
                If the prompt has nothing to do with food then the model will return nothing"},
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": str(item)
                    }
                ]
            }
        ]
    )
    return(completion.choices[0].message)

def getNutrientsHomemade(item):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are given a homeade food item. Since these are homeade they will be healthier\
                and have better nutritional statistics than fast food items. \
                Break down the nutrients of this item in the following categories: \
                Calories, Protein, Fat, Cholesterol, Sodium, Vitamin D, Calcium, Potassium, Iron, Zinc \
                Ensure the ingredients and prices are all comma-separated. All entries must have a valu and ingredient. An example \
                entry would be: Calories: 100g, Protein: 20g, ... \
                If the prompt has nothing to do with food then the model will return nothing"},
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": str(item)
                    }
                ]
            }
        ]
    )
    return(completion.choices[0].message)

def getNutrientsFastFood(place, item):
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are given a fast food item and the restaurant it is from. \
                Take into account the grease and other less healthy cooking practices commonly used by fast food restaurants. \
                Provide a breakdown of the nutrients in the item using the following categories, with each value including its unit: \
                Calories (kcal), Protein (g), Fat (g), Cholesterol (mg), Sodium (mg), Vitamin D (mcg), Calcium (mg), Potassium (mg), Iron (mg), Zinc (mg). \
                Each nutrient should be followed by a comma. Ensure all nutrient values match in unit type and format. \
                For example: Calories: 100 kcal, Protein: 20 g, Fat: 10 g, Cholesterol: 30 mg, Sodium: 500 mg, Vitamin D: 2 mcg, Calcium: 100 mg, Potassium: 300 mg, Iron: 5 mg, Zinc: 1 mg. \
                If the prompt is unrelated to food, respond with an empty message. Both sides must have same number of rows, have the same units, same number of unit places, etc"},
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"restaurant: {str(place)} item: {str(item)}"
                    }
                ]
            }
        ]
        )
        return(completion.choices[0].message)

def getEstimatedPrice(place, item):
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are given a fast food item and a fast food place the item is from. \
                Estimate the price of this item in dollars with two units for cents. Take into account this estimation is for a single person's order \
                Ususally these are around ten dollars. Return only this calculate $XX.XX and nothing more\
                If the prompt has nothing to do with food then the model will return nothing"},
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"restaurant: {str(place)} item: {str(item)}"
                    }
                ]
            }
        ]
        )
        return(completion.choices[0].message)



def getRecipe(item):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
         {
              "role": "system", "content":
                "You are providing recipe steps for a food item given a list of ingredients. All generated text should only be within the context of the recipe, do not expand on ideas. also attempt to format the recipe properly multiline and numbered, ingredient count listed."},
         {
              "role": "user",
                "content":
                [
                    {
                    "type": "text",
                    "text": f"item: {str(item)}"
                    }
                ]
         }
    ]
    )
    return(completion.choices[0].message)
     

@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    #message = ""
    if form.validate_on_submit():
            ingrRes = getIngredients(form.item.data)
            getIngredientsList = str(ingrRes.content)
            getIngredientsList = getIngredientsList.split(",")
            getIngredientsListRes= []
            
            for i in range(0, len(getIngredientsList), 2):
                getIngredientsListRes.append(getIngredientsList[i].strip())

            getPriceList = []
            if (len(getIngredientsList) > 1):
                for i in range(0, len(getIngredientsList), 2):
                    getPriceList.append(getIngredientsList[i+1].strip())
                
            getNutrientsHomemadeList = getNutrientsHomemade(form.item.data).content
            getNutrientsHomemadeList = getNutrientsHomemadeList.split(",")

            for i in range(0, len(getNutrientsHomemadeList)):
                getNutrientsHomemadeList[i] = getNutrientsHomemadeList[i].strip()

            getNutrientsFastList = getNutrientsFastFood(form.resturant.data, form.item.data).content
            getNutrientsFastList = getNutrientsFastList.split(",")

            for i in range(0, len(getNutrientsFastList)):
                getNutrientsFastList[i] = getNutrientsFastList[i].strip()

            print(getPriceList)
            total_sum = 0
            for i in getPriceList:
                print(float(i[1:]))
                if i[0] == '$':
                    total_sum += float(i[1:])
                else:
                    total_sum += float(i)

            getEstimatedPriceRes = getEstimatedPrice(form.resturant.data, form.item.data).content

            if getEstimatedPriceRes[0] == '$':
                getEstimatedPriceRes = float(getEstimatedPriceRes[1:])
            else:
                getEstimatedPriceRes = float(getEstimatedPriceRes)
            
            #name = form.name.data
            #if name.lower() not in "names":
            # empty the form field
            #form.name.data = ""
            # redirect the browser to another route and template
            return render_template("index2.html", form=form,\
                ingredients=getIngredientsListRes,\
                prices=getPriceList,\
                homemade=getNutrientsHomemadeList,\
                fastFood=getNutrientsFastList,\
                homeadePrice = total_sum, res = total_sum - getEstimatedPriceRes, user_Ingredient = True, Recipe = False,
                recipe= getRecipe(form.item.data).content)
        #else:
            #message = "That actor is not in our database."
    return render_template("index2.html", form=form, ingredients=[], user_Ingredient = False, Recipe = False, res = -1)

if __name__ == '__main__':
    app.run()