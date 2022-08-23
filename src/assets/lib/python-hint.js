const commonKeywords = [
    "as", "assert", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import",
    "lambda", "pass", "raise", "return",
    "try", "while", "with", "yield", "in"
  ];
  const commonBuiltins = [
    "abs", "all", "any", "bin", "bool", "bytearray", "callable", "chr",
    "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod",
    "enumerate", "eval", "filter", "float", "format", "frozenset",
    "getattr", "globals", "hasattr", "hash", "help", "hex", "id",
    "input", "int", "isinstance", "issubclass", "iter", "len",
    "list", "locals", "map", "max", "memoryview", "min", "next",
    "object", "oct", "open", "ord", "pow", "property", "range",
    "repr", "reversed", "round", "set", "setattr", "slice",
    "sorted", "staticmethod", "str", "sum", "super", "tuple",
    "type", "vars", "zip", "__import__", "NotImplemented",
    "Ellipsis", "__debug__"
  ];
  const PythonHint = commonKeywords.concat(commonBuiltins);
  
  export default PythonHint;