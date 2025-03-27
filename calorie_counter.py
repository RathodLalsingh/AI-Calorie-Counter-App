from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
import sys

load_dotenv()
client = OpenAI()

def get_calories_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are a dietitian. A user sends you an image of a mealo of the image and you tell them to how many calories count are in it. Use the following JSON in format:

{
    "reasoning": "reasoning for the total calories meals",
    "food_items": [
        {
            "name": "food item name",
            "calories": "calories in the food item meal"
        }
    ],
    "total": "total calories in the meal Count"
}"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "How many calories is in this meal?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
    )

    response_message = response.choices[0].message
    content = response_message.content

    return json.loads(content)

if __name__ == "__main__":
    image_path = sys.argv[1]
    calories = get_calories_from_image(image_path)
    print(json.dumps(calories, indent=4))
