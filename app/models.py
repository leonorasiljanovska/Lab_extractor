
from pydantic import BaseModel, Field
from typing import List, Optional, Union


class LaboratoryTest(BaseModel):
    parameter: str = Field(..., description="The parameter being measured")
    value: Optional[Union[float, str]] = Field(None, description="The test result value")
    reference_min: Optional[float] = Field(None, description="Lower bound of reference range")
    reference_max: Optional[float] = Field(None, description="Upper bound of reference range")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Full reference range as string")
    status: Optional[str] = Field(None, description="Normal/High/Low status")


class LaboratoryResults(BaseModel):
    tests: List[LaboratoryTest] = Field(default=[], description="List of test results")


class ExtractResponse(BaseModel):
    success: bool
    results: Optional[LaboratoryResults] = None
    error: Optional[str] = None
