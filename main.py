from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
KEY=os.getenv('OPEN_API_KEY')

client = OpenAI(api_key=KEY)


def calculatePrice(responseObject, inputPerM, outputperM):
    inputUnit = inputPerM / 1_000_000
    outputUnit = outputperM / 1_000_000

    inputUsed = responseObject.usage.prompt_tokens
    outputUsed = responseObject.usage.completion_tokens

    return inputUsed * inputUnit + outputUsed * outputUnit



def promptFormatterAgent(client, content):
    
    response = client.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[
            {"role": "system", "content": "You are a friendly chatbot"},
            {"role": "user", "content": content}
        ]
    )

    print(response.choices[0].message.content, '\n\n')
    print("Total Price: ", '$', calculatePrice(response, 0.05, 0.4))


def codeGeneratorAgent(client):
    pass




if __name__ == "__main__":
    promptFormatterAgent(client=client, content='Hello can you give me the capital of Russia please?')
