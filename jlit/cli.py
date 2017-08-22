from functools import partial
import subprocess
import sys

def _jin(name, value, env):
    if name in env:
        return env[name]
    else:
        return value

def parse_variables(var_string):
    """
    Parse variables in a dictionary form
    """

    vars = {}
    lines = [line for line in var_string.split(";") if line != ""]
    for line in lines:
        tokens = [token.strip() for token in line.split("=")]
        assert len(tokens) == 2
        vars[tokens[0]] = eval(tokens[1])

    return vars

def init(var_string=""):
    return partial(_jin, env=parse_variables(var_string))

def execute_notebook(notebook, var_string):
    script = notebook.replace(".ipynb", ".py")
    subprocess.run(f"jupyter nbconvert --to script {notebook}",
                   shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(["sed", "-i", f"s/jlit.init()/jlit.init(\"{var_string}\")/g", script])
    subprocess.run(["python", script])
    subprocess.run(f"rm {script}", shell=True)

def main():
    assert len(sys.argv) == 3, "Error in usage"
    execute_notebook(sys.argv[1], sys.argv[2])
