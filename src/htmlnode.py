class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        s = ""
        if self.props == None:
            return s
        for p in self.props.items():
            s += f' {p[0]}="{p[1]}"'
        return s

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("need a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    # TODO write test
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("need a tag")
        if self.children == None or self.children == []:
            raise ValueError("need children")

        s = ""
        for child in self.children:
            s += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{s}</{self.tag}>"

    # TODO write test
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
