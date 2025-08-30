from openai import OpenAI
import os
from dotenv import load_dotenv




def calculatePrice(responseObject, inputPerM, outputperM):
    inputUnit = inputPerM / 1_000_000
    outputUnit = outputperM / 1_000_000

    inputUsed = responseObject.usage.prompt_tokens
    outputUsed = responseObject.usage.completion_tokens

    return inputUsed * inputUnit + outputUsed * outputUnit



def promptFormatterAgent(client, content):
    
    sys_prompt = """
    You are a step-by-step math reasoning assistant.
    When given a user question, you must follow these rules strictly:

    Guardrail: Only respond if the user's query is mathematical in nature (arithmetic, algebra, geometry, calculus, probability, statistics, etc.).

    If the query is unrelated to mathematics (for example, about cooking, politics, philosophy, or general chit-chat), respond with:
    "This system only handles mathematical problem solving. Please provide a math-related question."

    Step Breakdown:

    Provide a maximum of 10 steps.

    Step 1 and Step 2 must explain the components of the question (what is being asked, what information is given, what concepts are involved).

    Steps 3 through 10 (as needed) must detail how to solve the problem step by step. Stop earlier if the solution is complete.

    Display Types: Each step must be explicitly tagged with one of the following types:

    TEXT → For plain explanations in words.

    LATEX → For mathematical equations, formulas, or expressions.

    ILLUSTRATION → For any non-text representation of the problem (for example, number lines, graphs, tables, unit circles, geometric diagrams, shaded areas under graphs).

    Formatting:
    Each step must follow this structure:

    (DISPLAY TYPE) STEP NUMBER. Step content

    Example:
    (LATEX) 3. The solution can be found using the equation x + 5 = 10

    Clarity: Keep each step concise but self-contained, so the user can follow the reasoning without external references.
    """


    response = client.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": content}
        ]
    )

    print(response.choices[0].message.content, '\n\n')
    print("Total Price: ", '$', calculatePrice(response, 0.05, 0.4))


def codeGeneratorAgent(client):
    pass




if __name__ == "__main__":

    load_dotenv()
    KEY=os.getenv('OPEN_API_KEY')

    client = OpenAI(api_key=KEY)
    
    promptFormatterAgent(client=client, content='What is the capital of Greenland?')
