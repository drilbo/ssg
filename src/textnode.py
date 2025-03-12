from enum import Enum
from htmlnode import LeafNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("not a valid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        s = node.text.split(delimiter)
        if len(s) % 2 == 0:
            raise Exception("invalid markdown, not closed")
        for i in range(len(s)):
            if s[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(s[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(s[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        split_nodes = []
        while extracted := extract_markdown_images(n.text):
            img_alt, img_url = extracted[0]
            sections = n.text.split(f"![{img_alt}]({img_url})", 1)
            if sections[0]:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            n.text = sections[1]
        if n.text != "":
            split_nodes.append(TextNode(n.text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        split_nodes = []
        while extracted := extract_markdown_links(n.text):
            link_text, link_url = extracted[0]
            sections = n.text.split(f"[{link_text}]({link_url})", 1)
            if sections[0]:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            n.text = sections[1]
        if n.text != "":
            split_nodes.append(TextNode(n.text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    tn = TextNode(text, TextType.TEXT)
    tn = split_nodes_delimiter([tn], "`", TextType.CODE)
    tn = split_nodes_delimiter(tn, "**", TextType.BOLD)
    tn = split_nodes_delimiter(tn, "_", TextType.ITALIC)
    tn = split_nodes_image(tn)
    tn = split_nodes_link(tn)
    return tn
