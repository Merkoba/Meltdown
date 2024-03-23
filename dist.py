import os
import shutil
import ast, astunparse
import random
import string
import json

from strip_hints import strip_file_to_string

outdir = "dist"
modir = "dist/meltdown"
program = "meltdown"

def random_word(length):
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    mode = "cons"

    def con() -> str:
        return random.choice(consonants)

    def vow() -> str:
        return random.choice(vowels)

    word = ""

    for _ in range(length):
        if mode == "vow":
            word += vow()
            mode = "cons"
        else:
            word += con()
            mode = "vow"

    return word

def nounstring():
    words = []

    for _ in range(random.randint(1, 18)):
        words.append(random_word(random.randint(2, 7)))

    return " ".join(words)

def process(input_file):
    clean_code = strip_file_to_string(input_file)
    lines = astunparse.unparse(ast.parse(clean_code)).split("\n")
    new_lines = []

    for line in lines:
        stripped_line = line.rstrip()
        if stripped_line:
            if stripped_line.lstrip()[:1] not in ("'", '"'):
                new_lines.append(stripped_line)
                whitespace = stripped_line[:len(stripped_line) - len(stripped_line.lstrip())]
                if random.randint(1, 7) == 1:
                    vals = nounstring()
                    text = f'{whitespace}# {vals}'
                    new_lines.append(text)


    new_code = "\n".join(new_lines)
    base_filename = os.path.basename(input_file)
    output_file = os.path.join(modir, base_filename)

    with open(output_file, "w") as f:
        f.write(new_code)

def main():
    if not outdir:
        return

    if os.path.exists(outdir):
        shutil.rmtree(outdir)

    os.mkdir(outdir)
    os.mkdir(modir)

    for root, dirs, files in os.walk(program):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                process(file_path)

    with open(os.path.join(modir, "__init__.py"), "w") as f:
        pass

    shutil.copy("setup.py", f"{outdir}/setup.py")
    shutil.copy("requirements.txt", f"{outdir}/requirements.txt")
    shutil.copy(f"{program}/manifest.json", f"{modir}/manifest.json")
    shutil.copy(f"{program}/icon.png", f"{modir}/icon.png")

    with open(f"{program}/manifest.json", "r") as file:
        manifest = json.load(file)

    version = manifest["version"].replace(".", "_")
    shutil.make_archive(f"meltdown_v_{version}", "gztar", outdir)

if __name__ == "__main__":
    main()