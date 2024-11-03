from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import secrets
import os
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from openai import OpenAI

client = OpenAI(api_key="KEY HERE")

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    item = StringField('Restaurant?', validators=[DataRequired(), Length(10, 40)])
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
                the ingredients and prices are all comma-separated. An example \
                entry would be: ingredient1, price1, ingredient2, price2, ..."},
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

def getNutrientsHomemade():
     pass

def getNutrientsFastFood():
     pass

def getRecipe():
     pass
     

@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    #message = ""
    if form.validate_on_submit():
            '''ingrRes = getIngredients(form.item.data)
            getIngredientsList = str(ingrRes.content)
            getIngredientsList = getIngredientsList.split(",")
            
            for i in range(0, len(getIngredientsList), 2):
                getIngredientsList[i] = getIngredientsList[i].strip()

            getPriceList = []
            for i in range(0, len(getIngredientsList), 2):
                getPriceList.append(getIngredientsList[i+1].strip())
                
            getNutrientsHomemadeList = []
            getNutrientsFastFoodList = []'''
            #name = form.name.data
            #if name.lower() not in "names":
            # empty the form field
            #form.name.data = ""
            # redirect the browser to another route and template
            return render_template("index2.html", form=form,\
                ingredients=["chicken breast", "flour", "breadcrumbs","egg", "oil", "salt", "pepper"],\
                prices=["1 dolla", "5 dolla", "2 dolla","0 cents", "a soul", "1 dolla", "a dolla"])
    
    '''            prices=getPriceList,\
                homemadeList=getNutrientsHomemadeList, \
                fastFoodList=getNutrientsFastFoodList'''
        #else:
            #message = "That actor is not in our database."
    return render_template("index2.html", form=form, ingredients=[])

if __name__ == '__main__':
    app.run()