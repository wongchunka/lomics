<h1>Lomics - Large Language Models for Omics Studies</h1>

<ul>
<li><strong>Version:</strong> v1.1</li>
<li><strong>Date:</strong> January 5, 2025</li>
<li><strong>Developers:</strong> Chun-Ka WONG, Ali CHOO, Eugene C. C. CHENG, Wing-Chun SAN, Kelvin Chak-Kong CHENG, Hung-Fat TSE, Jason Wing-Hon WONG (The University of Hong Kong)</li>
<li><strong>Contact:</strong> wongeck@hku.hk</li>
<li><strong>Web application:</strong> <a href="http://www.lomics.ai">http://www.lomics.ai</a></li>
</ul>

<h2>Introduction</h2>
    <p>Analyzing biological pathways is crucial in omics data research. Large language models (LLMs) now allow researchers to create custom pathways and gene sets specific to their research questions. These tailored sets are more compact than traditional libraries used in pathway enrichment analysis, which may reduce multiple hypothesis testing issues and potentially boost statistical power.</p>
    <p>Lomics (Large Language Models for Omics Studies) is a Python-based bioinformatics tool designed to simplify the creation of pathways and gene sets for transcriptomic analysis. The process involves three main steps:</p>
    <ol>
        <li>Identifying relevant pathways based on the researcher's specific inquiry</li>
        <li>Creating valid gene sets for each identified pathway</li>
        <li>Producing results in .GMX and .GMT format</li>
    </ol>
    <p>In addition to generating pathways and gene sets, Lomics provides explanations for its pathway selections. The tool ensures consistency and accuracy through iterative processes, JSON format validation, and verification of gene symbols using the HUGO Gene Nomenclature Committee (HGNC) standards.</p>
    <p>Lomics represents a significant step towards integrating LLMs into omics research, with the potential to enhance the specificity and efficiency of pathway analysis in the field.</p>

<h2>Installation</h2>

<pre><code>git clone https://www.github.com/wongchunka/lomics
cd lomics
pip install -r requirements.txt
</code></pre>

<h2>Settings</h2>

<p>By default, large language model (LLM) API calls are mediated via LiteLLM with Replicate cloud and OpenAI GPT-4o model. Configurations can be modified in setting.py, including:</p>
<ul>
  <li>API key</li>
  <li>Choice of model (visit <a href="https://github.com/BerriAI/litellm">LiteLLM repository</a> for details)</li>
</ul>

<p> Other Lomics setting that can adjusted in setting.py, including:</p>
<ul>
  <li>Number of pathways to be generated (default: 100)</li>
  <li>Number of genes to be generated (default: 100)</li>
  <li>Number of iterations for generating output (default: 10 for pathway and 3 for gene)</li>
</ul>

<h2>Run Lomics on command line interface (CLI)</h2>

<pre><code>python run.py --question "scientific question" --outputname "output file name" --outputdir "output file directory"
</code></pre>

<h2>Citation</h2>
<p>If Lomics is used for research, please cite:</p>
<pre><code>@misc{wong2024lomicsgenerationpathwaysgene,
      title={Lomics: Generation of Pathways and Gene Sets using Large Language Models for Transcriptomic Analysis}, 
      author={Chun-Ka Wong and Ali Choo and Eugene C. C. Cheng and Wing-Chun San and Kelvin Chak-Kong Cheng and Yee-Man Lau and Minqing Lin and Fei Li and Wei-Hao Liang and Song-Yan Liao and Kwong-Man Ng and Ivan Fan-Ngai Hung and Hung-Fat Tse and Jason Wing-Hon Wong},
      year={2024},
      eprint={2407.09089},
      archivePrefix={arXiv},
      primaryClass={q-bio.MN},
      url={https://arxiv.org/abs/2407.09089}, 
}</code></pre>