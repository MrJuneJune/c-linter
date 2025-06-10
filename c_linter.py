import os
import re
import sys

# Regex patterns
POINTER_SPACING_PATTERN = r'\b(\w+)\s*\*\s*(\w+)'
ELSE_BRACE_PATTERN = r'^(\s*)}\s*(else(?: if)?\b[^{]*)\s*{'
FUNCTION_BRACE_PATTERN = r'(.*\))\s*{\s*(.*)'
BRACE_ON_SAME_LINE_PATTERN = r'\)\s*{'
OPENING_BRACE_NOT_ALONE_PATTERN = r'[^\s].*{.*[^\s}]'
CLOSING_BRACE_NOT_ALONE_PATTERN = r'[^\s].*}.*[^\s{]'
INDENT_PATTERN = r'^\s*'

# Replacement patterns
POINTER_SPACING_REPLACEMENT = r'\1 *\2'

# Lint messages
MSG_POINTER_SPACING = "put '*' next to variable (e.g., 'int* x')"
MSG_BRACE_NEW_LINE = "'{' must be on a new line"
MSG_OPENING_BRACE_ALONE = "'{' should be on its own line"
MSG_CLOSING_BRACE_ALONE = "'}' should be on its own line"

# File extensions to process
C_EXTENSIONS = ('.c', '.h')

# Status messages
MSG_LINTING_COMPLETE = "✅ {} linting and formatting complete."
MSG_USAGE = "Usage: python c_linter.py <file_or_dir> <fix:true|false>"
MSG_FILE_NOT_FOUND = "❌ Error: {} is not a file or directory."

def print_lint_error(filename, lineno, message):
    """Helper function to print lint error messages in a consistent format."""
    print(f"{filename}:{lineno}: {message}")

def print_status(message, *args):
    """Helper function to print status messages."""
    print(message.format(*args))

def fix_pointer_spacing(line):
    """Fix patterns like: int* x -> int *x"""
    return re.sub(POINTER_SPACING_PATTERN, POINTER_SPACING_REPLACEMENT, line)

def fix_brace_placement(lines):
    """Fix brace placement according to coding standards."""
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        indent = re.match(INDENT_PATTERN, line).group()
        
        # Keep lone braces
        if stripped in ("{", "}"):
            new_lines.append(line)
            continue
        
        # Special case: "} else {" or "} else if (...) {"
        match = re.match(ELSE_BRACE_PATTERN, line)
        if match:
            indent = match.group(1)
            control = match.group(2).strip()
            new_lines.append(f"{indent}}}\n")
            new_lines.append(f"{indent}{control}\n")
            new_lines.append(f"{indent}{{\n")
            continue
        
        # General case: "(...) {"
        match = re.search(FUNCTION_BRACE_PATTERN, line)
        if match:
            prefix = match.group(1)
            suffix = match.group(2)
            new_lines.append(f"{prefix}\n")
            new_lines.append(f"{indent}{{\n")
            if suffix.strip():
                new_lines.append(f"{indent}{suffix.strip()}\n")
            continue
        
        new_lines.append(line)
    
    return new_lines

def lint_and_fix_c_file(filename):
    """Lint and fix a C file by applying formatting rules."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Apply pointer fix first
    lines = [fix_pointer_spacing(line) for line in lines]
    
    # Then apply brace placement fix
    lines = fix_brace_placement(lines)
    
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print_status(MSG_LINTING_COMPLETE, filename)

def lint_c_code(filename):
    """Check a C file for linting issues and report them."""
    with open(filename) as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        lineno = i + 1
        
        if re.search(POINTER_SPACING_PATTERN, line):
            print_lint_error(filename, lineno, MSG_POINTER_SPACING)
        
        if re.search(BRACE_ON_SAME_LINE_PATTERN, line):
            print_lint_error(filename, lineno, MSG_BRACE_NEW_LINE)
        
        if re.search(OPENING_BRACE_NOT_ALONE_PATTERN, line):
            print_lint_error(filename, lineno, MSG_OPENING_BRACE_ALONE)
        
        if re.search(CLOSING_BRACE_NOT_ALONE_PATTERN, line):
            print_lint_error(filename, lineno, MSG_CLOSING_BRACE_ALONE)

def get_all_c_files(path):
    """Recursively find all C source and header files in a directory."""
    c_files = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(C_EXTENSIONS):
                c_files.append(os.path.join(root, f))
    return c_files

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_status(MSG_USAGE)
        sys.exit(1)
    
    target = sys.argv[1]
    do_fix = sys.argv[2].lower() == "true"
    
    files_to_lint = []
    if os.path.isfile(target):
        # Check if the file has a valid C extension
        if target.endswith(C_EXTENSIONS):
            files_to_lint = [target]
        else:
            print_status("❌ Error: {} is not a C or header file.", target)
            sys.exit(1)
    elif os.path.isdir(target):
        files_to_lint = get_all_c_files(target)
    else:
        print_status(MSG_FILE_NOT_FOUND, target)
        sys.exit(1)
    
    for file in files_to_lint:
        if do_fix:
            lint_and_fix_c_file(file)
        lint_c_code(file)

