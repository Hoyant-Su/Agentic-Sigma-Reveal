# Agentic Sigma-Reveal

Task-conditioned initial workspace observations for agent harnesses, with ancestor-closed tree selection under a character budget.

```bash
pip install git+https://github.com/Hoyant-Su/Agentic-Sigma-Reveal.git
sigma-reveal ./workspace --task "Analyze sales.csv with Python" --budget-chars 2400
```

```python
from sigma_reveal import reveal
from sigma_reveal_reference import METHOD

context = reveal("./workspace", "Analyze sales.csv with Python", budget_chars=2400)
method_reference = METHOD
```

The selector preserves the released method's scoring and tree optimization. Line costs are rounded up to 16-character buckets. The default budget is 2400 characters. Only the initial observation is generated; the receiving harness supplies subsequent observations.

## Local MCP

```bash
pip install 'agentic-sigma-reveal[mcp] @ git+https://github.com/Hoyant-Su/Agentic-Sigma-Reveal.git'
sigma-reveal-mcp --workspace ./workspace
```

The stdio server exposes `select_workspace_context(task, budget_chars)` and `describe_method()`. Selection returns the workspace view and original method reference, including BibTeX. The `sigma-reveal://reference` resource returns the BibTeX alone. Client configuration after installation:

```json
{
  "mcpServers": {
    "sigma-reveal": {
      "command": "sigma-reveal-mcp",
      "args": ["--workspace", "/path/to/task-workspace"]
    }
  }
}
```

The server binds to the workspace supplied at startup. Use a prepared workspace whose files may be read by the model. The MCP interface rejects symbolic links and special files in the inspected tree. Direct Python and CLI selection retain the original traversal behavior, including following symlinks. Keep the workspace unchanged during selection. File previews are untrusted task data.

The selector inspects up to four levels and reads up to 160 bytes per file for an 80-character first-line preview. The view budget constrains rendered output; it does not bound the number of directory entries inspected. Dynamic programming scales with tree size and the square of the budget in buckets.

## Harness integration

See [initial workspace context selection](examples/workspace-context-selection.md) for selection rules, budget units, and the relationship to repository maps.

`examples/deepagents_initial_context.py` supplies a static selected view to Deep Agents before its first action. See `examples/deepagents.md` for invocation and scope.

## Method reference

The reference identifies the original observation method (section 3.2). The paper formulates a token-budget objective; its released implementation uses character buckets, as exposed by this package.

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
