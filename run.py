from pathway import lomics_pathway
from gene import lomics_gene
from report import lomics_report
from setting import *

def main():
    parser = argparse.ArgumentParser(description='Lomics: Large Language Models for Omic Studies v1.0', epilog='python run.py --question "scientific question" --outputname "output file name" --outputdir "output file directory"')
    parser.add_argument('--question', type=str, required=True, help='Scientific question')
    parser.add_argument('--outputname', type=str, required=True, help='Output file name')
    parser.add_argument('--outputdir', type=str, required=True, help='Output file directory')
    args = parser.parse_args()
    input_question = args.question
    output_name = args.outputname
    output_dir = args.outputdir
    lomics_pathway(input_question, var_num_pathway, var_llm, var_maxtoken, var_temp, var_iterate_pathway, var_max_concurrent_call, var_max_attempt, output_name, output_dir)
    lomics_gene(input_question, var_llm, var_maxtoken, var_temp, var_iterate_gene, var_num_gene, var_max_concurrent_call, var_max_attempt, output_name, output_dir)
    lomics_report(input_question, var_llm, var_maxtoken, var_temp, var_max_attempt, output_name, output_dir)

if __name__ == "__main__":
    main()