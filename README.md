# C Code Linter and Formatter

Simple python script that lints and automatically fixes C code formatting issues according to specific coding standards.

## Usage

```bash
python c_linter.py <file_or_directory> <fix:true|false>
```

### Parameters

- `<file_or_directory>`: Path to a single C file or directory containing C files
- `<fix:true|false>`: Whether to automatically fix issues or just report them

## Requirements

- Python 3.x

## Coding Standards Enforced

### Pointer Declaration Format
```c
// ✅ Correct
int *ptr;
char *str;

// ❌ Incorrect
int* ptr;
int*ptr;
char * str;
```

### Brace Placement
```c
// ✅ Correct
if (condition)
{
    // code
}

void function()
{
    // code
}

// ❌ Incorrect
if (condition) {
    // code
}

void function() {
    // code
}
```

## File Structure

The script processes only files with `.c`  and `.h` extension and will recursively search directories for C files.

## Limitations

- Focused on specific formatting rules (pointer spacing and brace placement)
- Does not perform syntax validation or advanced code analysis
- May not handle all edge cases in complex C code structures
