"""
This module is responsible for interacting with the LLM via API. 
"""

import instructor
from openai import OpenAI
from dotenv import load_dotenv
from schema import LLMQueryOutput, LLMFinalOutput
from fields import fields

# Load API key and patch the instructor client
load_dotenv()
client = instructor.from_openai(OpenAI())

# List of indexed field names ['associatedsequences', 'barcodevalue', 'basisofrecord', 'catalognumber', ...
field_names = [field['field_name'] for field in fields]

systemPrompt = """
    You are an LLM that specializes in converting natural language queries to iDigBio queries in iDigBio query format. 
    You should use scientific names whenever possible. If there are multiple relevant scientificnames, search for them all. 
    
    Example output: rq = {{"stateprovince":"Florida","scientificname":"anura"}}
    You can search for multiple values within a field by separating the values with a comma. Single values should be a text string. 
    Example with multiple values for a single field: {{"stateprovince":"Florida","scientificname":["anura","araneae"]}}
    For example, if the user asks a question about Spiders, you should query for scientificname "Araneae".
    
    You can utilize the following fields in your query: {0}. Consider the user's natural language input, take your time to determine the relevat fields to be used, and when you're ready
    generate the query.
""".format(field_names)


def generate_query(question: str) -> LLMQueryOutput:
    """
    Parses a natural language question and returns an llm-generated query.

    Parameters:
    question (str): A question related to Biodiversity occurrence records.

    Returns:
    LLMQueryOutput (dict): A dictionary containing the original question and the query generated. 
    """
    return client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        response_model=LLMQueryOutput,
        messages=[
        {
            "role": "system",
            "content": systemPrompt
        },
        {
            "role": "user",
            "content": question
        }
    ],
    )


initial_response = generate_query("Fetch all the galax urceolata collected in the united states.").model_dump(exclude_none=True)
print(initial_response['rq'])
