# Count the total number of lines
cd meltdown
find . -type f -name "*.py" ! -name "pyperclip.py" ! -name "tests.py" -exec wc -l {} \; | awk '{t+=$1} END {print t}'
