from setting import *

def lomics_gene(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, var_max_concurrent_call, var_max_attempt, output_name, output_dir):
    ############################################################################################################
    # Functions
    async def prompt_gene(input_question, var_num_gene, var_llm, var_maxtoken, var_temp, pathway, limit, var_max_attempt):
        prompt = f'''Instructions:
            - You are a bioinformatician analyzing transcriptomic data. 
            - You are tasked with selecting [ {str(var_num_gene)} ] genes for analysis of [ {pathway} ] pathway. 
            - Your scientific question is: [ {input_question} ]. 
            - You are requred to output a JSON object only.
            - Genes have to be HGNC gene symbol. 
            - You must not return any words before and after the JSON object.
            - JSON object schema is specified in the following pydantic description:
                class pydantic_gene(BaseModel):'''
        for i in range(var_num_gene):
            prompt += f'''
            gene{i+1}: str = Field(description="gene{i+1}")'''
        for i in range(var_max_attempt):
            try:
                response = await llm_call(prompt, var_llm, var_maxtoken, var_temp, limit)
                return response
            except:
                continue
        return None

    async def json_schema_gene(llm_output, var_num_gene):
        fields = {}
        for i in range(1, var_num_gene+1):
            column_name = f"gene{i}"
            fields[column_name] = (str, Field(..., title=column_name))
        pydantic_gene_object = create_model("genes", **fields, __base__=BaseModel)
        try:
            json_dict = loads(llm_output)
            validated_data = pydantic_gene_object.parse_obj(json_dict)
            return llm_output
        except ValueError as e:
            print("Pydantic validation error:", e)
            return None

    async def batch_prompt_gene(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, pathway, ls_hgnc, limit, var_max_attempt):
        tasks = [prompt_gene(input_question, var_num_gene, var_llm, var_maxtoken, var_temp, pathway, limit, var_max_attempt) for _ in range(var_iterate_gene)]
        ls_llm_output = await asyncio.gather(*tasks)
        tasks = [json_schema_gene(llm_output, var_num_gene) for llm_output in ls_llm_output]
        ls_validated_llm_output = await asyncio.gather(*tasks)
        df_output = pd.DataFrame(columns=["pathway", "gene", "succeeded_iterate", "var_iterate_gene", "llm", "temp", "num_pathway", "num_gene", "hgnc_valid"])
        succeeded_iterate = 0
        for validated_llm_output in ls_validated_llm_output:
            if validated_llm_output is not None:
                try:
                    json_dict = loads(validated_llm_output)
                    json_ls = [value for key, value in json_dict.items()]
                    json_ls = [re.sub(r',', '', value) for value in json_ls]
                    df_output_partial = pd.DataFrame(json_ls, columns=["gene"])
                    df_output_partial["pathway"] = re.sub(r',', '', pathway)
                    df_output_partial["succeeded_iterate"] = succeeded_iterate
                    df_output_partial["var_iterate_gene"] = var_iterate_gene
                    df_output_partial["llm"] = var_llm
                    df_output_partial["temp"] = var_temp
                    df_output_partial["num_pathway"] = var_num_pathway
                    df_output_partial["num_gene"] = var_num_gene
                    df_output = pd.concat([df_output, df_output_partial])
                    succeeded_iterate += 1
                except:
                    continue
        df_output.loc[df_output["gene"].isin(ls_hgnc), "hgnc_valid"] = True
        df_output.loc[~df_output["gene"].isin(ls_hgnc), "hgnc_valid"] = False
        return df_output

    async def batch_prompt_gene_iterate(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, ls_pathway, ls_hgnc, var_max_concurrent_call, var_max_attempt, output_name, output_dir):
        limit = asyncio.Semaphore(var_max_concurrent_call)
        tasks = [batch_prompt_gene(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, pathway, ls_hgnc, limit, var_max_attempt) for pathway in ls_pathway]
        ls_df_output = await asyncio.gather(*tasks)
        df_output = pd.concat(ls_df_output, ignore_index=True)
        df_output.to_csv(os.path.join(output_dir, output_name + "_gene.csv"), index=False)

    ############################################################################################################
    # Execution
    with open(path_hgnc, 'r', encoding='utf-8') as file:
        json_hgnc = load(file)

    ls_hgnc = [item['symbol'] for item in json_hgnc['response']['docs']]
    df_pathway = pd.read_csv(os.path.join(output_dir, output_name + "_pathway.csv"))
    ls_pathway = df_pathway['pathway'].value_counts().nlargest(var_num_pathway).index.tolist()
    asyncio.run(batch_prompt_gene_iterate(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, ls_pathway, ls_hgnc, var_max_concurrent_call, var_max_attempt, output_name, output_dir))
