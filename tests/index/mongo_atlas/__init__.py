# Licensed to the LF AI & Data foundation under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
from typing import Callable

from pydantic import Field

from docarray import BaseDoc
from docarray.typing import NdArray

N_DIM = 10


class SimpleSchema(BaseDoc):
    text: str = Field(index_name='text_index')
    number: int
    embedding: NdArray[10] = Field(dim=10, index_name="vector_index")


class SimpleDoc(BaseDoc):
    embedding: NdArray[N_DIM] = Field(dim=N_DIM, index_name="vector_index_1")


class NestedDoc(BaseDoc):
    d: SimpleDoc
    embedding: NdArray[N_DIM] = Field(dim=N_DIM, index_name="vector_index")


class FlatSchema(BaseDoc):
    embedding1: NdArray = Field(dim=N_DIM, index_name="vector_index_1")
    embedding2: NdArray = Field(dim=N_DIM, index_name="vector_index_2")


def assert_when_ready(callable: Callable, tries: int = 10, interval: float = 2):
    """
    Retry callable to account for time taken to change data on the cluster
    """
    while True:
        try:
            callable()
        except AssertionError as e:
            tries -= 1
            if tries == 0:
                raise RuntimeError("Retries exhausted.") from e
            time.sleep(interval)
        else:
            return
