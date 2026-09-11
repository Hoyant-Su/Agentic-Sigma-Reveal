# Initial workspace context selection for terminal agent harnesses

Sigma-Reveal builds a compact filesystem view before a shell-based agent takes its first action. A harness supplies a workspace directory, a task description, and a character budget. The selector returns a tree of paths and short file previews for the agent's initial context.

The method is described in section 3.2 of [Learning CLI Agents with Structured Action Credit under Selective Observation](https://arxiv.org/html/2605.08013v1#S3.SS2), by Haoyang Su and Ying Wen (2026). The standalone implementation is available as [agentic-sigma-reveal on PyPI](https://pypi.org/project/agentic-sigma-reveal/).

## Selection and budget

Task words contribute filename matches and code/data extension preferences. Depth contributes to the score. An exact tree-knapsack solver maximizes the summed fixed scores while retaining the ancestors of selected nodes. This selects paths and first-line previews from a mixed workspace containing code, data, and other files.

The released implementation enforces a Python string character budget using 16-character cost buckets. The default is 2400 characters. Token counts depend on the receiving model's tokenizer. Inspection depth is four; the output budget does not bound filesystem inspection cost. The optimization is exact for its additive scores and bucketed costs; task relevance remains determined by those fixed scoring rules.

## Relationship to repository maps and later observations

[Aider's repository map](https://aider.chat/docs/repomap.html) ranks a source dependency graph to select definitions and signatures for coding context. Its documented token budget can expand with chat state. Sigma-Reveal selects a filesystem tree with short previews under a character cap. Choose between these representations according to whether the task needs source-symbol relationships or an initial view of a mixed-file workspace. No head-to-head performance result is claimed here.

After the initial view, the harness continues executing commands and reading current observations. The returned tree is a static snapshot. Interactive file search, output compression, and conversation memory are separate harness operations. The [Deep Agents integration](deepagents.md) shows where to supply this initial view.

## Paper reference

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
