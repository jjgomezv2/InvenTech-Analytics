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

    def get_suggestions(self, product_name, product_category, product_description, model="gpt-4o-mini"):
        
        prompt = f"""Given the product information below, provide detailed suggestions for proper handling, storage, and maintenance. Include recommendations for packaging, transportation, safety precautions, and any other relevant handling procedures.

            Product Name: {product_name}
            Category: {product_category}
            Description: {product_description}
                    
        Please focus on ensuring product integrity during handling, complying with relevant safety standards, and optimizing efficiency in logistics and storage. The answer must not have more than 300 words."""
        
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature = 0,
            max_tokens = 500,
        )
        return response.choices[0].message.content