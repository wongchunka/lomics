# Lomics - Large Language Models for Omics Sciences
# Version v1.0
# Date: June 30, 2024
# Developers: Chun-Ka WONG, Ali CHOO, Eugene C. C. CHENG, Wing-Chun SAN, Kelvin Chak-Kong CHENG, Hung-Fat TSE, Jason Wing-Hon WONG (The University of Hong Kong)
# http://www.lomics.ai

import os
from glob import glob
import pandas as pd
from litellm import acompletion
import asyncio
from json import loads, load
from pydantic import BaseModel, Field, create_model
import re
import csv
import argparse

os.environ["REPLICATE_API_KEY"] = ""
var_llm = "replicate/meta/meta-llama-3-70b-instruct"
var_maxtoken = 3600
var_temp = 0
var_max_concurrent_call = 100
var_num_pathway = 40
var_iterate_pathway = 10
var_num_gene = 40
var_iterate_gene = 5
var_max_attempt = 20
lomics = "v1"
current_dir = os.path.dirname(os.path.abspath(__file__))
path_hgnc = os.path.join(current_dir, "resources", "hgnc_20240507.json")

async def llm_call(prompt, var_llm, var_maxtoken, var_temp, limit):
    try:
        async with limit:
            response = await acompletion(
                model=var_llm, 
                messages = [{ 
                    "role": "user",
                    "content": prompt,
                    "max_new_tokens": var_maxtoken,
                    "temperature": var_temp,
                    "top_k": 50,
                    "top_p": 0.9,
                    "length_penalty": 1,
                    "presence_penalty": 0,
                }],
                max_tokens = var_maxtoken
            )
            print(response)
            response = response['choices'][0]['message']['content']
            print(response)
            return response
    except Exception as e:
        print(e)
        return None