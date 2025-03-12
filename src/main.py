from textnode import TextNode, TextType
from genpage import generate_page, generate_pages_recursive
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    copy_static(dir_path_static, dir_path_public)
    print("~#%#~ generating pages ~#%#~")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )
def copy_static(src, dst):
    if not os.path.exists(src):
        raise Exception("source directory doesnt exist")
    srcpaths = os.listdir(src)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    recur_cp(src, dst)

def recur_cp(src, dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"cp {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"mkdir {dst_path}")
            os.mkdir(dst_path)
            recur_cp(src_path, dst_path)
    
    


main()


