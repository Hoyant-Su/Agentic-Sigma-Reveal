import tempfile
import unittest
from pathlib import Path

from mcp import Client

from sigma_reveal import reveal
from sigma_reveal_mcp import create_server
from sigma_reveal_reference import BIBTEX


class MCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_selection_and_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'sales.csv').write_text('year,revenue\n2025,12\n')
            async with Client(create_server(root)) as client:
                result = await client.call_tool('select_workspace_context', {'task': 'Analyze sales.csv', 'budget_chars': 80})
                self.assertFalse(result.is_error)
                self.assertEqual(result.structured_content['context'], reveal(directory, 'Analyze sales.csv', 80))
                self.assertEqual(result.structured_content['method']['bibtex'], BIBTEX)
                reference = await client.read_resource('sigma-reveal://reference')
                self.assertEqual(reference.contents[0].text, BIBTEX)

    async def test_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'link').symlink_to(root)
            async with Client(create_server(root)) as client:
                result = await client.call_tool('select_workspace_context', {'task': 'Inspect files'})
                self.assertTrue(result.is_error)


if __name__ == '__main__':
    unittest.main()
