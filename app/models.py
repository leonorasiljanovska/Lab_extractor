# from pydantic import BaseModel, Field
# from typing import List, Optional
#
#
# class LaboratoryTest(BaseModel):
#     parameter: str = Field(..., description="The parameter being measured (e.g., 'Blood Sugar').")
#     value: float = Field(..., description="The numerical result of the test.")
#     reference_min: Optional[float] = Field(None, description="The lower bound of the normal reference range.")
#     reference_max: Optional[float] = Field(None, description="The upper bound of the normal reference range.")
#     unit: str = Field(..., description="The unit of measurement (e.g., 'mmol/L', 'mg/dL').")
#     semantic_class: Optional[str] = Field(None,
#                                           description="The semantic class from an ontology (e.g., LOINC, SNOMED CT) for the parameter.")
#
#
# class LaboratoryResults(BaseModel):
#     tests: List[LaboratoryTest] = Field(..., description="List of laboratory test results.")
#
#
# class ExtractResponse(BaseModel):
#     success: bool
#     results: Optional[LaboratoryResults] = None
#     error: Optional[str] = None
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
