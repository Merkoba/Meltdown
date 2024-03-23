import os
import shutil
from strip_hints import strip_file_to_string
import ast, astunparse

outdir = "dist"

def process(input_file):
    base_filename = os.path.basename(input_file)
    output_file = os.path.join(outdir, base_filename)
    clean_code = strip_file_to_string(input_file)

    lines = astunparse.unparse(ast.parse(clean_code)).split("\n")
    new_lines = []

    for line in lines:
        stripped_line = line.rstrip()
        if stripped_line:
            if stripped_line.lstrip()[:1] not in ("'", '"'):
                new_lines.append(stripped_line)

    new_code = "\n".join(new_lines)

    with open(output_file, "w") as f:
        f.write(new_code)

def main():
    if not outdir:
        return

    if os.path.exists(outdir):
        shutil.rmtree(outdir)

    os.mkdir(outdir)

    for root, dirs, files in os.walk("meltdown"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                process(file_path)

    with open(os.path.join(outdir, "__init__.py"), "w") as f:
        pass

    shutil.copy("meltdown/manifest.json", f"{outdir}/manifest.json")
    shutil.copy("meltdown/icon.png", f"{outdir}/icon.png")

if __name__ == "__main__":
    main()