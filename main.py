from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
KEY=os.getenv('OPEN_API_KEY')

client = OpenAI()


def promptFormatterAgent():
    pass


def codeGeneratorAgent():
    pass




if __name__ == "__main__":
    pass
