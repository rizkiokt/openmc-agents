from utils.objects import Code

# store python code from pydantic object code into a file
# include imports, prefix, and code
def store_code(code: Code, file_path: str):
    with open(file_path, "w") as f:
        f.write(f"'''\n{code.prefix}\n'''\n")
        f.write(code.imports)
        f.write(code.code)

