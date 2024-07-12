<h1>Lomics - Large Language Models for Omics Studies</h1>

<p><strong>Version:</strong> v1.0<br>
<strong>Date:</strong> June 30, 2024<br>
<strong>Developers:</strong> Chun-Ka WONG, Ali CHOO, Eugene C. C. CHENG, Wing-Chun SAN, Kelvin Chak-Kong CHENG, Hung-Fat TSE, Jason Wing-Hon WONG (The University of Hong Kong)<br>
<strong>Contact:</strong> wongeck@hku.hk</p>
<strong>Web application:</strong> <a href="http://www.lomics.ai">http://www.lomics.ai</a>

<h2>Installation</h2>

<pre><code>git clone https://www.github.com/wongchunka/lomics
cd lomics
pip install -r requirements.txt
</code></pre>

<h2>Settings</h2>

<p>By default, large language model (LLM) API calls are mediated via LiteLLM with Replicate cloud and LLama-3 70B instruct model. Configurations can be modified in setting.py, including:</p>
<ul>
  <li>API key</li>
  <li>Choice of model (visit <a href="https://github.com/BerriAI/litellm">LiteLLM repository</a> for details)</li>
</ul>

<p> Other Lomics setting that can adjusted in setting.py, including:</p>
<ul>
  <li>Number of pathways to be generated</li>
  <li>Number of genes to be generated</li>
  <li>Number of iterations for generating output</li>
</ul>

<h2>Run Lomics on command line interface (CLI)</h2>

<pre><code>python run.py --question "scientific question" --outputname "output file name" --outputdir "output file directory"
</code></pre>