import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
         node = TextNode("This is a text node", TextType.BOLD)
         node2 = TextNode("This is a text node", TextType.BOLD)
         self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is 1 text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode("This is boring", TextType.BOLD)
        node2 = TextNode("This is boring", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_no_url_eq(self):
        node = TextNode("This", TextType.TEXT, None)
        node2 = TextNode("This", TextType.TEXT)
        self.assertEqual(node, node2)
    
    def test_no_url_not_eq(self):
        node = TextNode("T", TextType.LINK, "")
        node = TextNode("T", TextType.LINK)

    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("TESTES", TextType.TEXT)
        html1 = text_node_to_html_node(node)
        html2 = LeafNode(None, "TESTES")
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)
        
    def test_text_node_to_html_node_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html1 = text_node_to_html_node(node)
        html2 = LeafNode("b", "bold")
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("fancy", TextType.ITALIC)
        html1 = text_node_to_html_node(node)
        html2 = LeafNode("i", "fancy")
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_code(self):
        node = TextNode("code", TextType.CODE)
        html1 = text_node_to_html_node(node)
        html2 = LeafNode("code", "code")
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_link(self):
        node = TextNode("boot.dev", TextType.LINK, "https://boot.dev")
        html1 = text_node_to_html_node(node)
        html2 = LeafNode("a","boot.dev",{"href": "https://boot.dev"})
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_img(self):
        node = TextNode("ALT", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html1 = text_node_to_html_node(node)
        html2 = LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "ALT"})
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_exception(self):
        node = TextNode("oops", "not a textype")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(sn, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_code_bad(self):
        node = TextNode("This is text with `only opening code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_code_2short(self):
        node = TextNode("This is text with `no text after the code block`", TextType.TEXT)
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(sn, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("no text after the code block", TextType.CODE),
            TextNode("", TextType.TEXT),
            ]
        )

    def test_split_nodes_code_3short(self):
        node = TextNode("`no text before or after code block`", TextType.TEXT)
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(sn, [
            TextNode("", TextType.TEXT),
            TextNode("no text before or after code block", TextType.CODE),
            TextNode("", TextType.TEXT),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("big **bold** words", TextType.TEXT)
        sn = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(sn, [
            TextNode("big ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
            ]
        )

    def test_split_nodes_italic(self):
        node = TextNode("fa*ncy*", TextType.TEXT)
        sn = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(sn, [
            TextNode("fa", TextType.TEXT),
            TextNode("ncy", TextType.ITALIC),
            TextNode("", TextType.TEXT),
            ]
        )

    def test_split_nodes_code_nodelim(self):
        node = TextNode("no delimiter here", TextType.BOLD)
        sn = split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(sn, [
            TextNode("no delimiter here", TextType.BOLD),
            ]
        )

    def test_split_nodes_all3(self):
        node = TextNode("this `has` **a lot** going *on*", TextType.TEXT)
        snc = split_nodes_delimiter([node], "`", TextType.CODE)
        snb = split_nodes_delimiter(snc, "**", TextType.BOLD)
        sni = split_nodes_delimiter(snb, "*", TextType.ITALIC)
        self.assertEqual(sni, [
            TextNode("this ", TextType.TEXT),
            TextNode("has", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("a lot", TextType.BOLD),
            TextNode(" going ", TextType.TEXT),
            TextNode("on", TextType.ITALIC),
            TextNode("", TextType.TEXT),
            ]
        )

   
if __name__ == "__main__":
    unittest.main()

