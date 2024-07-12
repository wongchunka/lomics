from setting import *

def lomics_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, var_iterate_pathway, var_max_concurrent_call, var_max_attempt, output_name, output_dir):
    ############################################################################################################
    # Functions
    async def prompt_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, limit, var_max_attempt):
        prompt = f'''Instructions:
            - You are a bioinformatician analyzing transcriptomic data. 
            - You are tasked with selecting [ {str(var_num_pathway)} ] pathways for analysis. 
            - Your scientific question is: [ {input_question} ]. 
            - You are requred to output a JSON object only.
            - You must not return any words before and after the JSON object.
            - JSON object schema is specified in the following pydantic description:
                class pydantic_pathway(BaseModel):'''
        for i in range(var_num_pathway):
            prompt += f'''
                    pathway{i+1}: str = Field(description="pathway{i+1}")'''
        for attempt in range(var_max_attempt):
            try:
                response = await llm_call(prompt, var_llm, var_maxtoken, var_temp, limit)
                return response
            except:
                continue
        return None

    async def json_schema_pathway(llm_output, var_num_pathway):
        fields = {}
        for i in range(1, var_num_pathway+1):
            column_name = f"pathway{i}"
            fields[column_name] = (str, Field(..., title=column_name))
        pydantic_pathway_object = create_model("pathways", **fields, __base__=BaseModel)
        try:
            json_dict = loads(llm_output)
            validated_data = pydantic_pathway_object.parse_obj(json_dict)
            return llm_output
        except ValueError as e:
            print("Pydantic validation error:", e)
            return None
        
    async def batch_prompt_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, var_iterate_pathway, var_max_concurrent_call, var_max_attempt, output_name, output_dir):
        limit = asyncio.Semaphore(var_max_concurrent_call)
        tasks = [prompt_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, limit, var_max_attempt) for _ in range(var_iterate_pathway)]
        ls_llm_output = await asyncio.gather(*tasks)
        tasks = [json_schema_pathway(llm_output, var_num_pathway) for llm_output in ls_llm_output]
        ls_validated_llm_output = await asyncio.gather(*tasks)
        df_output = pd.DataFrame(columns=["pathway", "succeeded_iterate", "var_iterate_pathway", "llm", "temp", "num_pathway"])
        succeeded_iterate = 0
        for validated_llm_output in ls_validated_llm_output:
            if validated_llm_output is not None:
                json_dict = loads(validated_llm_output)
                json_ls = [value for key, value in json_dict.items()]
                json_ls = [re.sub(r',', '', value) for value in json_ls]
                df_output_partial = pd.DataFrame(json_ls, columns=["pathway"])
                df_output_partial["succeeded_iterate"] = succeeded_iterate
                df_output_partial["var_iterate_pathway"] = var_iterate_pathway
                df_output_partial["llm"] = var_llm
                df_output_partial["temp"] = var_temp
                df_output_partial["num_pathway"] = var_num_pathway
                df_output = pd.concat([df_output, df_output_partial])
                succeeded_iterate += 1
        df_output.to_csv(os.path.join(output_dir, output_name + "_pathway.csv"), index=False)

    ############################################################################################################
    # Execution
    asyncio.run(batch_prompt_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, var_iterate_pathway, var_max_concurrent_call, var_max_attempt, output_name, output_dir))
