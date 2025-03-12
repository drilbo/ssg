import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks3(self):
        md = "what the fuck else am I supposed to test here"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["what the fuck else am I supposed to test here"],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

this is yet another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "this is yet another paragraph",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading1(self):
        bt = block_to_block_type("# this is a heading!")
        self.assertEqual(bt, BlockType.HEADING)

    def test_block_to_block_type_heading6(self):
        bt = block_to_block_type("###### this is a heading!")
        self.assertEqual(bt, BlockType.HEADING)

    def test_block_to_block_type_heading8(self):
        bt = block_to_block_type("######### this is a heading!")
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_block_to_block_type_code1(self):
        bt = block_to_block_type("```this is a codeblock!```")
        self.assertEqual(bt, BlockType.CODE)

    def test_block_to_block_type_code2(self):
        bt = block_to_block_type("```\nthis is a codeblock!\n```")
        self.assertEqual(bt, BlockType.CODE)

    def test_block_to_block_type_quote1(self):
        bt = block_to_block_type(">this is a quote")
        self.assertEqual(bt, BlockType.QUOTE)

    def test_block_to_block_type_quote2(self):
        bt = block_to_block_type(">line one\n>line2\n>line3")
        self.assertEqual(bt, BlockType.QUOTE)

    def test_block_to_block_type_quote_no(self):
        bt = block_to_block_type(">line one\nline2\nline3")
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_block_to_block_type_ul1(self):
        bt = block_to_block_type("- line one\n- line2\n- line3")
        self.assertEqual(bt, BlockType.UL)

    def test_block_to_block_type_ul_no(self):
        bt = block_to_block_type("- line one\n-line2\nline3")
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_block_to_block_type_ol1(self):
        bt = block_to_block_type("1. line one\n2. line2\n3. line3")
        self.assertEqual(bt, BlockType.OL)

    def test_block_to_block_type_ol_no(self):
        bt = block_to_block_type("1. line one\n1. line2\n2. line3")
        self.assertEqual(bt, BlockType.PARAGRAPH)

        

class TestMarkdownToHtmlNode(unittest.TestCase):
    maxDiff = None
    def test_markdown_to_html_node_ok(self):
        node = markdown_to_html_node("just some text")
       
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertMultiLineEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headers(self):
        md = """
# h1

### h3

###### h6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>h1</h1><h3>h3</h3><h6>h6</h6></div>"
        )

    def test_quote(self):
        md = "> quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>quote</blockquote></div>")

    def test_ul(self):
        md = """
- this
- that
- other
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this</li><li>that</li><li>other</li></ul></div>"
        )

    def test_ol(self):
        md = """
1. one
2. two
3. three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
