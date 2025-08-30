from openai import OpenAI
import os
from dotenv import load_dotenv

# Current Chosen is gpt-5-nano-2025-08-7
CHOSEN_MODEL_INPUT_TOKEN_PRICE_PER_M = 0.05
CHOSEN_MODEL_OUTPUT_TOKEN_PRICE_PER_M = 0.4


def calculatePrice(responseObject, inputPerM, outputperM):
    inputUnit = inputPerM / 1_000_000
    outputUnit = outputperM / 1_000_000

    inputUsed = responseObject.usage.prompt_tokens
    outputUsed = responseObject.usage.completion_tokens

    return inputUsed * inputUnit + outputUsed * outputUnit



def promptFormatterAgent(client, content) -> tuple:
    global CHOSEN_MODEL_INPUT_TOKEN_PRICE_PER_M, CHOSEN_MODEL_OUTPUT_TOKEN_PRICE_PER_M

    
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
        # Add Assistant & User Examples Here
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": content}
        ]
    )

    messageContent = response.choices[0].message.content
    agentPrice = calculatePrice(response, CHOSEN_MODEL_INPUT_TOKEN_PRICE_PER_M, CHOSEN_MODEL_OUTPUT_TOKEN_PRICE_PER_M)
    

    return messageContent, agentPrice


def codeGeneratorAgent(client, content, prevAgentPrice):
    global CHOSEN_MODEL_INPUT_TOKEN_PRICE_PER_M, CHOSEN_MODEL_OUTPUT_TOKEN_PRICE_PER_M

    sys_prompt = """
    You are a Manim code generation assistant.
    Your role is to take structured step-by-step outputs produced by the promptFormatterAgent and convert them into Manim code that visually illustrates each step. Follow these rules strictly:

    Guardrail:

    Only generate valid Python code using the Manim library.

    Do not generate unrelated code (e.g., file I/O, networking, database operations, operating system commands).

    If the input steps are not in the required structured format (with (DISPLAY TYPE) STEP NUMBER. Step content), respond with:
    "This system only generates Manim code from valid step-by-step mathematical reasoning steps. Please provide structured steps."

    Step-to-Scene Mapping:

    Each step provided must be represented as a separate Manim scene.

    There must be adequate pauses between scenes (e.g., using self.wait(2) or similar) so the viewer has time to absorb each step.

    Scenes must be sequential — no two steps should overlap, collide, or overwrite each other. Once a step’s scene is complete, the screen should be cleared before the next step begins.

    Display Type Handling:

    TEXT steps: Render as on-screen text (Text or MarkupText).

    LATEX steps: Render using MathTex.

    ILLUSTRATION steps: Render using the appropriate Manim primitives (e.g., NumberLine, Axes, Circle, Table, shaded areas).

    Always preserve the order and integrity of the original steps.

    Formatting Requirements:

    Each generated script must be a valid Python module runnable with Manim.

    Import only necessary modules from Manim (from manim import *).

    Organize output so each scene corresponds to one step. Name scenes systematically, e.g., Step1Scene, Step2Scene, etc.

    Include adequate pauses (self.wait()) at the end of each scene.

    Clarity:
    Keep the code minimal and clean, focusing only on what is needed to represent the steps faithfully. Avoid decorative or extra animations unless explicitly required by the step content.
    """


    response = client.chat.completions.create(
        model="gpt-5-nano-2025-08-07",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": content}
        ]
        
    )

    messageContent = response.choices[0].message.content
    agentPrice = calculatePrice(response, CHOSEN_MODEL_INPUT_TOKEN_PRICE_PER_M, CHOSEN_MODEL_OUTPUT_TOKEN_PRICE_PER_M)
    totalPrice = agentPrice + prevAgentPrice


    return messageContent, agentPrice, totalPrice


def main():
    # Sample workflow: UserInput -> PromptFormatterAgent -> CodeGeneratorAgent
    userInput = input('What would you like to learn today?\n')
    
    formattedPrompt = promptFormatterAgent(client=client, content=userInput)
    print('Steps generated by promptFormatterAgent:')
    print(formattedPrompt[0], '\n')
    print('Price of Formatting Agent: $', formattedPrompt[1])


    generatedCode = codeGeneratorAgent(client=client, content=formattedPrompt[0], prevAgentPrice=formattedPrompt[1])
    print('Code generated by codeGeneratorAgent:')
    print(generatedCode[0], '\n')
    print('Price of Coding Agent: $', generatedCode[1])
    print('Total Price of all Agents: $', generatedCode[2])


if __name__ == "__main__":

    load_dotenv()
    KEY=os.getenv('OPEN_API_KEY')

    client = OpenAI(api_key=KEY)

    main()

    



