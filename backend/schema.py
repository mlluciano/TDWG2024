"""
This module provides pydantic schema used to craft and validate LLM responses.
"""

from pydantic import Field, BaseModel, model_validator, ValidationInfo, AfterValidator
from typing import Optional, List, Union
from datetime import date
from fields import fields
import requests
from typing_extensions import Annotated

field_names = [field['field_name'] for field in fields]


class GeoPoint(BaseModel):
    """
    This schema represents a location on earth. 
    """
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)

def common_name_must_exist(s: str) -> str:
    url = f"https://api.checklistbank.org/vernacular?q={s}"
    res = requests.get(url)
    data = res.json()
    print(data)
    if data['empty'] == True:
        raise ValueError(f"Common name '{s}' does not exist.")
    
    return s

# class QueryStringSchema(BaseModel):
#     default_field: str = None
#     query: 

class QueryPart(BaseModel):
    field: Optional[str] = None  # Optional, can override default field
    value: str

class LogicalExpression(BaseModel):
    operator: str  # 'AND' or 'OR'
    values: list[str]
    # expressions: List[Union['LogicalExpression', QueryPart]]

    # Pydantic models require this configuration for recursive models
    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (tuple,)

class QueryString(BaseModel):
    default_field: str
    query: Union[QueryPart, LogicalExpression]

# class Query(BaseModel):
#     query_string: QueryString

class FieldValuePair(BaseModel):
    field: str
    value: str

class Expression(BaseModel):
    operator: str # 'AND' or 'OR'
    pairs: list[FieldValuePair]

class Q(BaseModel):
    expressions: list[Expression] 








class IDBQuerySchema(BaseModel):
    """
    This schema represents the iDigBio Query Format. 
    """
    associatedsequences: Optional[str] = None
    barcodevalue: Optional[str] = None
    basisofrecord: Optional[str] = None
    catalognumber: Optional[str] = None
    class_: Optional[str] = Field(default=None, alias='class')
    collectioncode: Optional[str] = None
    collectionid: Optional[str] = None
    collectionname: Optional[str] = None
    collector: Optional[str] = None
    commonname: Annotated[Optional[str], AfterValidator(common_name_must_exist)] = None
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






class LLMQueryOutput(BaseModel):
    """
    This schema represents the output containing the LLM-generated iDigBio query. 
    """
    input: str = Field(..., description="This field should contain the user's original input verbatim.")
    rq: Q = Field(..., description="This is the iDigBio Query in ElasticSearch 2.4 query string format and should contain the query generated from the user's plain text input.")


class LLMFinalOutput(BaseModel):
    """
    This schema represents the final response to the user. It should cite iDigBio data from the executed query. 
    """
    final_answer: str = Field(..., description="This response should be crafted using the data from the system prompt.")
