from pydantic import BaseModel, Field, confloat, conint, conlist
from typing import List
from .operations import Lottie, LottieOperation


class RequestParameters(BaseModel):
    animation: Lottie = Field(..., description='source animation')
    operations: List[LottieOperation] = Field(..., description='list of operations')


class Response(BaseModel):
    animation: Lottie = Field(..., description='result animation')
