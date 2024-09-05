import os
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv

class Handling_suggestions:
    _ = load_dotenv('openAI.env')
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openAI_api_key'),
    )

    def get_suggestions(self, product_name, product_category, product_description,prompt, model="gpt-4o-mini"):
        
        prompt = f""""""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content