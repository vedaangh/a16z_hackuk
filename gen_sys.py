"""
The entire website will be generated in the web_dir directory.

"""
import os
import shutil





def plan_design():
    # simply prompt the LLM. Provide it with search tools.
    # Come up with a step-by-step plan for the website.
    pass

def initial_code():
    pass

def refine_code():
     pass

def generate_code():
    pass

def test_code():
    pass

def clear_web_dir():
     # Clear the web_dir directory
    web_dir = "web_dir"
    if os.path.exists(web_dir):
        shutil.rmtree(web_dir)
    os.makedirs(web_dir)
    
def main():
     
    
