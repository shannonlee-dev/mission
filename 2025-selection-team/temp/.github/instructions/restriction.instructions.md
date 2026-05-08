---
applyTo: '**'
---

## Restrictions

### Library Usage Rules
- You must not use any external libraries or packages other than Python's built-in commands.
- For reading and organizing CSV files, you must use the pandas library.
- For creating and saving images, you may use external libraries.
- Results must be saved as DataFrame objects or PNG images.

### Coding Style Guide (PEP 8 Compliance)
- You must check and follow Python's coding style guide.
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)

#### String Representation
- Use single quotes `''` as the default for string representation.
- However, use double quotes `""` only when necessary, such as when the string contains single quotes.

#### Spacing and Indentation
- Use spaces around assignment operators like `foo = (0,)` with spaces before and after the `=`.
- Use spaces for indentation as the default.

#### Naming Conventions
- **Function Names**: Write in lowercase, and for names with two or more words, separate each word with an underscore (`_`).
- **Function and Variable Names**: Define names that do not conflict with Python's built-in reserved words.
- **Class Names**: Use CapWord style, starting with a capital letter, and if the name consists of two or more words, all subsequent words should also start with a capital letter.

#### Comments and Documentation
- All comments within the code must be written in Korean.
- All docstrings and internal documentation must be written in Korean.
- Function descriptions, variable explanations, and inline comments should use Korean language.
- Only function names, variable names, and class names should remain in English following the naming conventions above.

### Execution Quality
- All code must execute without warning messages.
