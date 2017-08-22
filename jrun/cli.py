import subprocess
import sys

def help():
    return "\n".join([
        " jrun",
        " ----",
        " Usage: jrun <notebook> [<var-definition-string>]",
        " Examples:",
        "   jrun notebook.ipynb \"name = 'var'; items = [1, 2]\" ",
        "   jrun notebook.ipynb"
    ])

def isnotebook():
    """
    Check if we are running in the notebook
    """

    try:
        return get_ipython().__class__.__name__ == "ZMQInteractiveShell"
    except NameError:
        return False

def jin(name, value):
    """
    Wrap around a variable to allow changing it from command line
    """

    if isnotebook():
        # Take the value directly from the notebook
        return value
    else:
        # Parse command line arguments for value
        # Defaults to provided value
        args = parse_variables(sys.argv[1])
        if name in args:
            return args[name]
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
        assert len(tokens) == 2, "Error in parsing variables"
        vars[tokens[0]] = eval(tokens[1])

    return vars

def execute_notebook(notebook, var_string):
    script = notebook.replace(".ipynb", ".py")
    subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook],
                   stderr=subprocess.DEVNULL)
    subprocess.run(["python", script, var_string])
    subprocess.run(f"rm {script}", shell=True)

def main():
    if len(sys.argv) not in [2, 3]:
        print(help())
        sys.exit(1)

    if len(sys.argv) == 2:
        var_string = ""
    else:
        var_string = sys.argv[2]
    execute_notebook(sys.argv[1], var_string)
