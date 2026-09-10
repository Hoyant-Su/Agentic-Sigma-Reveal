import argparse
import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

from sigma_reveal import _MAX_DEPTH, reveal
from sigma_reveal_reference import BIBTEX, METHOD


def validate_workspace(root: Path) -> None:
    if not root.is_dir():
        raise ValueError('workspace must be an existing directory')
    for directory, dirs, files in os.walk(root):
        depth = len(Path(directory).relative_to(root).parts)
        if depth >= _MAX_DEPTH:
            dirs.clear()
            continue
        for name in dirs + files:
            path = Path(directory) / name
            if path.is_symlink() or not (path.is_dir() or path.is_file()):
                raise ValueError('MCP workspace must contain only regular files and directories')


def create_server(workspace: Path) -> MCPServer:
    root = workspace.resolve(strict=True)
    server = MCPServer('Sigma-Reveal workspace context')

    @server.tool(structured_output=True)
    def select_workspace_context(task: str, budget_chars: int = 2400) -> dict[str, Any]:
        """Select a static initial workspace view and return the method's original paper reference."""
        validate_workspace(root)
        return {'context': reveal(str(root), task, budget_chars), 'method': METHOD}

    @server.tool(structured_output=True)
    def describe_method() -> dict[str, Any]:
        """Describe Sigma-Reveal's initial workspace selection method, scope, and original BibTeX."""
        return METHOD

    @server.resource('sigma-reveal://reference', mime_type='text/plain')
    def reference() -> str:
        """Original paper BibTeX for Sigma-Reveal workspace observation."""
        return BIBTEX

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description='Local Sigma-Reveal MCP server')
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    create_server(args.workspace).run()


if __name__ == '__main__':
    main()
