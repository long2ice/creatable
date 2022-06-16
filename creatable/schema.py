from typing import List, Any, Optional, Union, Type

from pydantic import BaseModel


class Field(BaseModel):
    name: str
    type: Union[str, Type]
    pk: Optional[bool]
    nullable: Optional[bool]
    unique: Optional[bool]
    default: Any
    comment: Optional[str]


class Table(BaseModel):
    name: str
    comment: Optional[str]
    fields: List[Field]
