import os

from blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("no title!")

def generate_page(from_path, template_path, dest_path):
    print(f"generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        mdfile = from_file.read()
    with open(template_path) as template_file:
        tfile = template_file.read()
    html = markdown_to_html_node(mdfile).to_html()
    title = extract_title(mdfile)
    tf = tfile.replace("{{ Title }}", title)
    nf = tf.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as dest:
        dest.write(nf)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)
    
    for f in content_files:
        if os.path.isfile(os.path.join(dir_path_content, f)):
            if f.endswith(".md"):
                generate_page(
                    os.path.join(dir_path_content, f),
                    template_path,
                    os.path.join(dest_dir_path, f.rstrip(".md") + ".html"),
                )
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, f),
                template_path,
                os.path.join(dest_dir_path, f)
            )