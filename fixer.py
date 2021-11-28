import os
from typing import List

IN_FOLDER = "./in/"
OUT_FOLDER = "./out/"

ANIMATION_NODE = "node dummy {tile_name}a\n"
END_NODE = "donemodel {tile_name}"

DUMMY_ANIMATION = [
    "\n",
    "#DUMMY_ANIMATION_FIX\n",
    "newanim tiledefault {tile_name}\n",
    "  length 0.0\n",
    "  transtime 0.0\n",
    "  animroot {tile_name}\n",
    "  node dummy {tile_name}\n",
    "    parent NULL\n",
    "  endnode\n",
    "doneanim tiledefault {tile_name}\n",
    "\n",
]

DUMMY_ANIMATION_COMMENT = DUMMY_ANIMATION[1]

def get_mdl_files() -> List[str]:
    """
    Fetch all mdl files in in_folder.
    """
    files = []
    for in_file in os.listdir(IN_FOLDER):
        if in_file.endswith(".mdl"):
            files.append(in_file)
    return files

def get_mdl_needs_fix(tile_name: str, content: List[str]) -> bool:
    """
    Return if a mdl has an animation node but no animations.
    """    
    animation_node = ANIMATION_NODE.format(tile_name=tile_name)   
    
    has_animation_node = False
    has_no_animations = True
    
    if animation_node in content:        
        has_animation_node = True

    if any("newanim" in content_line for content_line in content):
        has_no_animations = False

    return has_animation_node and has_no_animations

def add_dummy_animation(tile_name: str, content: List[str]) -> List[str]:
    """
    Add dummy animation add end of mdl.
    """
    end_node = END_NODE.format(tile_name=tile_name)          
        
    for line in DUMMY_ANIMATION:
        line = line.format(tile_name=tile_name)

        try:
            idx = content.index(end_node)
        except ValueError:
            idx = content.index(end_node + "\n")

        content.insert(idx, line)

    return content   

def get_file_content(in_file: str) -> List[str]:
    """
    Return list of all lines in given file.

    Return empty list if Decode Error is raised.
    """
    with open(f"{IN_FOLDER}{in_file}", "r") as mdl:
        try:
            content = mdl.readlines()
        except UnicodeDecodeError as error:
            print(f"Could not decode {in_file} and got following error msg: {str(error)}")
            content = []
    
    return content

def set_file_content(in_file: str, content: List[str]):
    """
    Write given content to given file.
    """
    with open(f"{OUT_FOLDER}{in_file}", "w+") as mdl:                
        mdl.writelines(content)


def fix_transparancy():
    """
    Iterate through all mdl files and add animation if needed.
    """
    files = get_mdl_files()
    
    for in_file in files:
        
        content = get_file_content(in_file)
                
        if not content:
            continue

        tile_name = in_file.split('.')[0]

        if get_mdl_needs_fix(tile_name, content): 

            content = add_dummy_animation(tile_name, content)

            set_file_content(in_file, content)

            print(f"Added dummy animation to file {in_file}")

def get_model_has_dummy_animation(content: List[str]) -> bool:
    """
    Return if dummy animation was added to file.
    """
    return DUMMY_ANIMATION_COMMENT in content

def remove_dummy_animation(tile_name: str, content: List[str]) -> List[str]:
    """
    Remove all lines from dummy aninmation node.

    Verify each line. If one line fails, animation might have been edited so
    raise error so mdl will be skipped.
    """
    end_node = END_NODE.format(tile_name=tile_name)
    
    for line in reversed(DUMMY_ANIMATION):
        line = line.format(tile_name=tile_name)
        
        try:
            idx = content.index(end_node)
        except ValueError:
            idx = content.index(end_node + "\n")
        
        if line == content[idx - 1]:
            content.pop(idx - 1)
        else:
            raise ValueError

    return content

def remove_transparancy_fix():
    """
    Iterate through all mdl files and remove animation if present.
    """
    files = get_mdl_files()
    
    for in_file in files:
        
        content = get_file_content(in_file)
                
        if not content:
            continue

        tile_name = in_file.split('.')[0]

        if get_model_has_dummy_animation(content):

            try:
                remove_dummy_animation(tile_name, content)
            except ValueError:
                print(f"Dummy Animation on file {in_file} seems to have changed. File was skipped.")
                continue

            set_file_content(in_file, content)

            print(f"Removed dummy animation from file {in_file}")

