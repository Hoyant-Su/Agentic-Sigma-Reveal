# Deep Agents initial workspace context

Use sigma-Reveal to select a task-conditioned initial filesystem observation before a Deep Agents run. The selector preserves ancestors and solves a tree knapsack over additive rendering costs. Its budget uses 16-character buckets. The task, prompt, and later tool outputs have separate context costs.

Install the package and Deep Agents in a Python environment, then install the LangChain integration for your chosen model provider:

```bash
python -m pip install "git+https://github.com/Hoyant-Su/Agentic-Sigma-Reveal.git" deepagents
```

For an OpenAI-compatible provider, install `langchain-openai` and configure that provider's credentials in your environment. From a checkout of this repository, run:

```bash
python examples/deepagents_initial_context.py ./workspace \
  --task "Find the CSV processing script and explain its inputs" \
  --model "$AGENT_MODEL" \
  --budget-chars 2400
```

Set `AGENT_MODEL` to your configured LangChain `provider:model` identifier. Invocation calls the configured model and gives it filesystem read/write tools within the workspace. Choose a task workspace whose contents may be sent to that provider. This example uses `FilesystemBackend` with virtual paths; shell execution requires a separate backend integration.

For application integration, call `prepare_run(workspace, task, model, budget_chars)` from [deepagents_initial_context.py](deepagents_initial_context.py). It returns the compiled agent and initial message dictionary. Model execution starts with `agent.invoke(inputs)`. Pass either a provider identifier or a configured LangChain chat model. The selected view is produced once; later file observations come from the framework's tools.

Graph construction and initial observation assembly were checked with `deepagents==0.7.13` and `langchain-openai==1.6.2` without model invocation. This integration has no task-success or token-efficiency evaluation. Framework reference: [Deep Agents backends](https://docs.langchain.com/oss/python/deepagents/backends).

## Method source

Sigma-Reveal is described in Section 3.2, “sigma-Reveal Context Harness,” of [Learning CLI Agents with Structured Action Credit under Selective Observation](https://arxiv.org/html/2605.08013v1#S3.SS2). This integration exposes its initial-observation selector. The paper also studies structured action credit and training, which are outside this example's implementation.

```bibtex
@article{su2026structuredactioncredit,
  title = {Learning CLI Agents with Structured Action Credit under Selective Observation},
  author = {Su, Haoyang and Wen, Ying},
  year = {2026},
  journal = {arXiv preprint arXiv:2605.08013},
  doi = {10.48550/arXiv.2605.08013},
  url = {https://arxiv.org/abs/2605.08013}
}
```
