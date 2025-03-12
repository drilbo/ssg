import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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
        html2 = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
        self.assertEqual(html1.tag, html2.tag)
        self.assertEqual(html1.value, html2.value)
        self.assertEqual(html1.props, html2.props)

    def test_text_node_to_html_node_img(self):
        node = TextNode(
            "ALT",
            TextType.IMAGE,
            "https://www.boot.dev/img/bootdev-logo-full-small.webp",
        )
        html1 = text_node_to_html_node(node)
        html2 = LeafNode(
            "img",
            "",
            {
                "src": "https://www.boot.dev/img/bootdev-logo-full-small.webp",
                "alt": "ALT",
            },
        )
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
        self.assertEqual(
            sn,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_code_bad(self):
        node = TextNode("This is text with `only opening code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_code_2short(self):
        node = TextNode(
            "This is text with `no text after the code block`", TextType.TEXT
        )
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            sn,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("no text after the code block", TextType.CODE),
            ],
        )

    def test_split_nodes_code_3short(self):
        node = TextNode("`no text before or after code block`", TextType.TEXT)
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            sn,
            [
                TextNode("no text before or after code block", TextType.CODE),
            ],
        )

    def test_split_nodes_bold(self):
        node = TextNode("big **bold** words", TextType.TEXT)
        sn = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            sn,
            [
                TextNode("big ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_split_nodes_italic(self):
        node = TextNode("fa*ncy*", TextType.TEXT)
        sn = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            sn,
            [
                TextNode("fa", TextType.TEXT),
                TextNode("ncy", TextType.ITALIC),
            ],
        )

    def test_split_nodes_code_nodelim(self):
        node = TextNode("no delimiter here", TextType.BOLD)
        sn = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            sn,
            [
                TextNode("no delimiter here", TextType.BOLD),
            ],
        )

    def test_split_nodes_all3(self):
        node = TextNode("this `has` **a lot** going *on*", TextType.TEXT)
        snc = split_nodes_delimiter([node], "`", TextType.CODE)
        snb = split_nodes_delimiter(snc, "**", TextType.BOLD)
        sni = split_nodes_delimiter(snb, "*", TextType.ITALIC)
        self.assertEqual(
            sni,
            [
                TextNode("this ", TextType.TEXT),
                TextNode("has", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("a lot", TextType.BOLD),
                TextNode(" going ", TextType.TEXT),
                TextNode("on", TextType.ITALIC),
            ],
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_md_images_1(self):
        img_list = extract_markdown_images(
            "This is text with a ![boot.dev logo](https://boot.dev/img/bootdev-logo-full-small.webp)"
        )
        self.assertEqual(
            img_list,
            [
                ("boot.dev logo", "https://boot.dev/img/bootdev-logo-full-small.webp"),
            ],
        )

    def test_extract_md_images_2(self):
        img_list = extract_markdown_images(
            "This is text with a ![boot.dev logo](https://boot.dev/img/bootdev-logo-full-small.webp) and this silly ![rick pic](https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertEqual(
            img_list,
            [
                ("boot.dev logo", "https://boot.dev/img/bootdev-logo-full-small.webp"),
                ("rick pic", "https://i.imgur.com/aKaOqIh.gif"),
            ],
        )

    def test_extract_md_images_empty(self):
        img_list = extract_markdown_images(
            "This doesn't even try to pretend to have an image"
        )
        self.assertEqual(img_list, [])

    def test_extract_md_links_1(self):
        link_list = extract_markdown_links(
            "This is text with a link [to boot.dev](https://boot.dev)"
        )
        self.assertEqual(
            link_list,
            [
                ("to boot.dev", "https://boot.dev"),
            ],
        )

    def test_extract_md_links_2(self):
        link_list = extract_markdown_links(
            "This is text with a link [to boot.dev](https://boot.dev) and [to youtube](https://youtube.com)"
        )
        self.assertEqual(
            link_list,
            [
                ("to boot.dev", "https://boot.dev"),
                ("to youtube", "https://youtube.com"),
            ],
        )

    def test_extract_md_links_empty(self):
        link_list = extract_markdown_links(
            "This doesn't even try to pretend to have a link"
        )
        self.assertEqual(link_list, [])


class TestSplitNodes(unittest.TestCase):
    def test_split_img1(self):
        node = TextNode("This has ![a logo](https://boot.dev/logo.gif)", TextType.TEXT)
        split = split_nodes_image([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a logo", TextType.IMAGE, "https://boot.dev/logo.gif"),
            ],
        )

    def test_split_img2(self):
        node = TextNode(
            "This has ![a logo](https://boot.dev/logo.gif) and ![something else](https://example.com/else.jpeg)",
            TextType.TEXT,
        )
        split = split_nodes_image([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a logo", TextType.IMAGE, "https://boot.dev/logo.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "something else", TextType.IMAGE, "https://example.com/else.jpeg"
                ),
            ],
        )

    def test_split_img_only_imgs(self):
        node = TextNode(
            "![a logo](https://boot.dev/logo.gif)![and more](local.gif)", TextType.TEXT
        )
        split = split_nodes_image([node])
        self.assertEqual(
            split,
            [
                TextNode("a logo", TextType.IMAGE, "https://boot.dev/logo.gif"),
                TextNode("and more", TextType.IMAGE, "local.gif"),
            ],
        )

    def test_split_img_more_text(self):
        node = TextNode(
            "This has ![a logo](https://boot.dev/logo.gif) and some more text",
            TextType.TEXT,
        )
        split = split_nodes_image([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a logo", TextType.IMAGE, "https://boot.dev/logo.gif"),
                TextNode(" and some more text", TextType.TEXT),
            ],
        )

    def test_split_img_just_text(self):
        node = TextNode("This is just text", TextType.TEXT)
        split = split_nodes_image([node])
        self.assertEqual(
            split,
            [
                TextNode("This is just text", TextType.TEXT),
            ],
        )

    # fuckin links
    def test_split_link1(self):
        node = TextNode("This has [a link](https://boot.dev/)", TextType.TEXT)
        split = split_nodes_link([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://boot.dev/"),
            ],
        )

    def test_split_link2(self):
        node = TextNode(
            "This has [a link](https://boot.dev/logo.gif) and [something else](https://example.com/else.jpeg)",
            TextType.TEXT,
        )
        split = split_nodes_link([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://boot.dev/logo.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "something else", TextType.LINK, "https://example.com/else.jpeg"
                ),
            ],
        )

    def test_split_link_only_links(self):
        node = TextNode(
            "[a link](https://boot.dev/logo.gif)[and link](local.gif)", TextType.TEXT
        )
        split = split_nodes_link([node])
        self.assertEqual(
            split,
            [
                TextNode("a link", TextType.LINK, "https://boot.dev/logo.gif"),
                TextNode("and link", TextType.LINK, "local.gif"),
            ],
        )

    def test_split_link_more_text(self):
        node = TextNode(
            "This has [a logo](https://boot.dev/logo.gif) and some more text",
            TextType.TEXT,
        )
        split = split_nodes_link([node])
        self.assertEqual(
            split,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a logo", TextType.LINK, "https://boot.dev/logo.gif"),
                TextNode(" and some more text", TextType.TEXT),
            ],
        )

    def test_split_link_just_text(self):
        node = TextNode("This is just text", TextType.TEXT)
        split = split_nodes_link([node])
        self.assertEqual(
            split,
            [
                TextNode("This is just text", TextType.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_default(self):
        tn = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertEqual(
            tn,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_somethingelse(self):
        tn = text_to_textnodes(
            "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertEqual(
            tn,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_bad(self):
        with self.assertRaises(Exception):
            text_to_textnodes("this has an '_' that somehow makes it bad")


if __name__ == "__main__":
    unittest.main()
