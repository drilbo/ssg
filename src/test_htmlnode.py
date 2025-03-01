import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_two(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev" target="_blank"'
        )

    def test_leafnode_no_props(self):
        node = LeafNode("p", "hello")
        self.assertEqual(node.to_html(), "<p>hello</p>")

    def test_leafnode_with_prop(self):
        node = LeafNode("a", "link", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">link</a>')

    def test_leafnode_no_value(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_no_tag(self):
        node = LeafNode(None, "poop")
        self.assertEqual(node.to_html(), "poop")

    def test_parentnode_base(self):
        node = ParentNode("div", [LeafNode("b", "test")])
        self.assertEqual(node.to_html(), "<div><b>test</b></div>")

    def test_parentnode_nase(self):
        node = ParentNode(
            "div",
            [LeafNode("b", "Bold"), ParentNode("p", [LeafNode("i", "Italic")])],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container"><b>Bold</b><p><i>Italic</i></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
