# Lomics - Large Language Models for Omics Sciences
# Version v1.1
# Date: January 5, 2025
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

os.environ["OPENAI_API_KEY"] = ""
var_llm = "gpt-4o"
var_maxtoken = 10000
var_temp = 0
var_max_concurrent_call = 100
var_num_pathway = 100
var_iterate_pathway = 10
var_num_gene = 100
var_iterate_gene = 3
var_max_attempt = 3
lomics = "v1.1"
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
                }],
                max_tokens = var_maxtoken,
                temperature = var_temp,
            )
            print("LLM response:")
            print(response)
            response = response['choices'][0]['message']['content']
            print("LLM message:")
            print(response)
            response = response[response.find('{'):response.rfind('}')+1]
            print("LLM message updated:")
            print(response)
            return response
    except Exception as e:
        print(e)
        return None