from pydantic import Field, BaseModel, model_validator, ValidationInfo
from typing import Optional, List, Union
from datetime import date
from openai import OpenAI
import instructor
import json
from dotenv import load_dotenv

load_dotenv()
client = instructor.from_openai(OpenAI())

class GeoPoint(BaseModel):
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)

class OutputQueryFormatSchema(BaseModel):
    associatedsequences: Optional[str] = None
    barcodevalue: Optional[str] = None
    basisofrecord: Optional[str] = None
    catalognumber: Optional[str] = None
    class_: Optional[str] = Field(default=None, alias='class')
    collectioncode: Optional[str] = None
    collectionid: Optional[str] = None
    collectionname: Optional[str] = None
    collector: Optional[str] = None
    commonname: Optional[str] = None
    continent: Optional[str] = None
    country: Optional[str] = None
    county: Optional[str] = None
    datecollected: Optional[date] = None
    datemodified: Optional[date] = None
    earliestperiodorlowestsystem: Optional[str] = None
    etag: Optional[str] = None
    eventdate: Optional[str] = None
    family: Optional[str] = None
    fieldnumber: Optional[str] = None
    genus: Optional[str] = None
    geopoint: Optional[GeoPoint] = None
    hasImage: Optional[bool] = None
    highertaxon: Optional[str] = None
    infraspecificepithet: Optional[str] = None
    institutioncode: Optional[str] = None
    institutionid: Optional[str] = None
    institutionname: Optional[str] = None
    kingdom: Optional[str] = None
    latestperiodorhighestsystem: Optional[str] = None
    locality: Optional[str] = None
    maxdepth: Optional[float] = None
    maxelevation: Optional[float] = None
    mediarecords: Optional[str] = None
    mindepth: Optional[float] = None
    minelevation: Optional[float] = None
    municipality: Optional[str] = None
    occurrenceid: Optional[str] = None
    order: Optional[str] = None
    phylum: Optional[str] = None
    recordids: Optional[str] = None
    recordnumber: Optional[str] = None
    recordset: Optional[str] = None
    scientificname: Optional[Union[str, List[str]]] = None
    specificepithet: Optional[str] = None
    stateprovince: Optional[Union[str, List[str]]] = None
    typestatus: Optional[str] = None
    uuid: Optional[str] = None
    verbatimeventdate: Optional[str] = None
    verbatimlocality: Optional[str] = None
    version: Optional[int] = None
    waterbody: Optional[str] = None

class QueryGenOutput(BaseModel):
    input: str = Field(..., description="This field should contain the user's original input verbatim.")
    rq: OutputQueryFormatSchema = Field(..., description="This is the iDigBio Query format and should contain the query generated from the user's plain text input.")

systemPrompt = """
    You are an LLM that specializes in converting natural language queries to iDigBio queries in iDigBio query format. 
    You should use scientific names whenever possible. If there are multiple relevant scientificnames, search for them all. 
    
    Example output: rq = {"stateprovince":"Florida","scientificname":"anura"}
    You can search for multiple values within a field by separating the values with a comma. Single values should be a text string. 
    Example with multiple values for a single field: {"stateprovince":"Florida","scientificname":["anura","araneae"]}
    For example, if the user asks a question about Spiders, you should query for scientificname "Araneae".
    
    You can utilize the following fields in your query: "${fieldNames}". Consider the user's natural language input, take your time to determine the relevat fields to be used, and when you're ready
    generate the query.
"""

def generateQuery(question: str) -> QueryGenOutput:
    return client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        response_model=QueryGenOutput,
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
        # validation_context={"text_chunk": context},
    )

initial_response = generateQuery("Which state in the US has the most bears?").model_dump(exclude_none=True)
print(initial_response['rq'])