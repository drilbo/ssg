from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def markdown_to_blocks(markdown):
    out = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block != "":
            out.append(block.strip())
    return out

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.search(r"^```.*```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^>", block):
        lines = block.split('\n')
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        return BlockType.PARAGRAPH
    elif re.match(r"^- ", block):
        lines = block.split('\n')
        if all(line.startswith("- ") for line in lines):
            return BlockType.UL
        return BlockType.PARAGRAPH
    elif re.match(r"^\d\. ", block):
        lines = block.split('\n')
        d = 1
        for line in lines:
            if not line.startswith(str(d) + '. '):
                return BlockType.PARAGRAPH
            d += 1
        return BlockType.OL    
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        bt = block_to_block_type(block)
        match bt:
            case BlockType.PARAGRAPH:
                o = block.replace("\n", " ")
                node = ParentNode("p", text_to_children(o))

            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == '#':
                        level += 1
                    else:
                        break
                content = block[level:].strip()
                tag = f"h{level}"
                node = ParentNode(tag, text_to_children(content))

            case BlockType.CODE:  #TODO this strips the \n from the end that is importatnly INSDIE the code block and shouldnt be touched
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                tn = TextNode(block[4:-3], TextType.TEXT)
                cn = ParentNode("code", [text_node_to_html_node(tn)])
                node = ParentNode("pre", [cn])

            case BlockType.QUOTE:
                lines = block.split("\n")
                clean = [line.lstrip('> ') for line in lines]
                o = " ".join(clean)
                node = ParentNode("blockquote", text_to_children(o))

            case BlockType.UL:
                lines = block.split("\n")
                list_items = []
                
                for line in lines:
                    if line.strip().startswith("- "):
                        list_item = ParentNode("li", text_to_children(line[2:]))
                        list_items.append(list_item)
                node = ParentNode("ul", list_items)

            case BlockType.OL:
                lines = block.split("\n")
                clean = []
                for line in lines:
                    if line.strip():
                        for i, char in enumerate(line):
                            if not (char.isdigit() or char == "." or char.isspace()):
                                clean.append(ParentNode("li", text_to_children(line[i:])))
                                break
                node = ParentNode("ol", clean)

        nodes.append(node)
    return ParentNode("div", nodes)

def text_to_children(text):
    nodes = []
    for node in text_to_textnodes(text):
        nodes.append(text_node_to_html_node(node))
    return nodes
