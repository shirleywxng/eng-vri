import os
from antlr4 import *
from matlab_parser.matlabLexer import matlabLexer
from matlab_parser.matlabParser import matlabParser

def is_valid_matlab(text):
    input_stream = InputStream(text)
    lexer = matlabLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = matlabParser(token_stream)
    parser.removeErrorListeners()  # Suppress console errors
    parser._syntaxErrors = 0       # Reset error count
    tree = parser.file_()
    return parser.getNumberOfSyntaxErrors() == 0

valid_count = 0
invalid_count = 0

for filename in os.listdir("completed_inputs"):
    path = os.path.join("completed_inputs", filename)
    with open(path, "r") as f:
        text = f.read().strip()

    valid = is_valid_matlab(text)
    if valid:
        valid_count += 1
    else:
        invalid_count += 1
    print(f"{filename}: {'VALID' if valid else 'INVALID'}")

print(f"\nTotal valid files: {valid_count}")
print(f"Total invalid files: {invalid_count}")
