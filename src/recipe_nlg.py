from openai import OpenAI

client = OpenAI(api_key="KEY HERE")
'''
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are providing recipe steps for a food item given a list of ingredients. All generated text should only be within the context of the recipe, do not expand on ideas."},
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Spaghetti, marinara sauce, chicken"
                }
            ]
        }
    ]
)

print(completion.choices[0].message)'''

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
                "text": "chicken nuggets"
                }
            ]
        }
    ]
)


print(completion.choices[0].message)