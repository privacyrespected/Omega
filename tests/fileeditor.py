import os
with open("tests/file.html",'r') as f:
    lines = f.read().splitlines()
    last_line= lines[-2]
    print(last_line)