from setting import *

def lomics_report(input_question, var_llm, var_maxtoken, var_temp, var_max_attempt, output_name, output_dir):
    ############################################################################################################
    # Functions
    async def prompt_explain(input_question, var_llm, var_maxtoken, var_temp, pathway, limit):
        prompt = f'''Instructions:
            - You are a bioinformatician analyzing transcriptomic data. 
            - You are tasked with explaining succinctly with 1 sentence why the following pathway: [ {pathway} ] is relevant for analysing the scientific question: [ {input_question} ].
            - You are requred to output a JSON object only.
            - You must not return any words before and after the JSON object only.
            - JSON object schema is specified in the following pydantic description:
                class pydantic_explain(BaseModel):
                    explain: str = Field(description="explain")'''
        try:
            response = await llm_call(prompt, var_llm, var_maxtoken, var_temp, limit)
            return response
        except:
            print(f"prompt_explain failed.")

    async def prompt_df_explain(input_question, var_llm, var_maxtoken, var_temp, pathway, var_max_attempt, limit):
        for i in range(var_max_attempt):
            try:
                explain = await prompt_explain(input_question, var_llm, var_maxtoken, var_temp, pathway, limit)
                json_dict = loads(explain)
                json_dict['explain'] = re.sub(r',', '', json_dict['explain']) 
                df_explain = pd.DataFrame([{"pathway": pathway, "pathway_explain": json_dict['explain']}])
                df_explain["llm"] = var_llm
                df_explain["temp"] = var_temp
                return df_explain
            except:
                print(f"prompt_df_explain failed.")

    async def batch_prompt_df_explain(input_question, var_llm, var_maxtoken, var_temp, var_max_attempt, output_name, output_dir):
        limit = asyncio.Semaphore(var_max_concurrent_call)
        tasks = [prompt_df_explain(input_question, var_llm, var_maxtoken, var_temp, pathway, var_max_attempt, limit) for pathway in ls_pathway]
        ls_df_explain = await asyncio.gather(*tasks)
        df_explain = pd.concat(ls_df_explain, ignore_index=True)
        df_explain.to_csv(os.path.join(output_dir, output_name + "_report.csv"), index=False)

    def output_gmx(df_gene, ls_pathway, gmx_output_path):
        pathway_dict = {}
        for pathway in ls_pathway:
            df_pathway = df_gene[df_gene["pathway"] == pathway]
            pathway_dict[pathway] = df_pathway["gene"].tolist()
            with open(gmx_output_path, "w") as f:
                for pathway, genes in pathway_dict.items():
                    f.write(f"{pathway}\t")
                    f.write('\t'.join(genes))
                    f.write("\n")
        return True

    def output_gmt(df_gene, ls_pathway, gmt_output_path):
        pathway_dict = {}
        for pathway in ls_pathway:
            df_pathway = df_gene[df_gene["pathway"] == pathway]
            pathway_dict[pathway] = df_pathway["gene"].tolist()
            with open(gmt_output_path, "w") as f:
                for pathway, genes in pathway_dict.items():
                    # Format: pathway_name    pathway_description   gene1   gene2   gene3...
                    f.write(f"{pathway}\t{pathway}\t")
                    f.write('\t'.join(genes))
                    f.write("\n")
        return True

    def transpose_file(gmx_output_path):
        with open(gmx_output_path, 'r') as input_file:
            reader = csv.reader(gmx_output_path, delimiter='\t')
            rows = [row for row in reader]
        max_length = max(len(row) for row in rows)
        transposed = [[row[i] if i < len(row) else '' for row in rows] for i in range(max_length)]
        with open(gmx_output_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file, delimiter='\t')
            for row in transposed:
                writer.writerow(row)

    def transpose_file(gmx_output_path):
        with open(gmx_output_path, 'r') as input_file:
            reader = csv.reader(input_file, delimiter='\t')
            rows = [row for row in reader]
        max_length = max(len(row) for row in rows)
        transposed = [[row[i] if i < len(row) else '' for row in rows] for i in range(max_length)]
        with open(gmx_output_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file, delimiter='\t')
            for row in transposed:
                writer.writerow(row)

    ############################################################################################################
    # Execution
    df_gene = pd.read_csv(os.path.join(output_dir, output_name + "_gene.csv"))
    ls_pathway = df_gene['pathway'].unique()
    asyncio.run(batch_prompt_df_explain(input_question, var_llm, var_maxtoken, var_temp, var_max_attempt, output_name, output_dir))
    df_gene = df_gene[df_gene['hgnc_valid'] == True]
    df_gene = df_gene.groupby(['pathway', 'gene']).size().reset_index(name='count')
    df_gene = df_gene.sort_values(['pathway', 'count'], ascending=[True, False])
    df_gene = df_gene.groupby('pathway').head(var_num_gene).reset_index(drop=True)
    output_gmx(df_gene, ls_pathway, os.path.join(output_dir, output_name + ".gmx"))
    output_gmt(df_gene, ls_pathway, os.path.join(output_dir, output_name + ".gmt"))
    transpose_file(os.path.join(output_dir, output_name + ".gmx"))