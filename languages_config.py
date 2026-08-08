"""
Configuration for multi-language support.
Includes explicit highlighting for variables and data types in Java, Python, C, and C++.
"""

LANGUAGES = {
    "python": {
        "extensions": [".py"],
        "rules": [
            # Standard Keywords (Blue)
            (r'\b(def|class|if|elif|else|while|for|import|from|as|try|except|finally|with|lambda|return|pass|break|continue|None|True|False)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(\#.*)', "comment"),
            # Python Built-ins and Types (Purple)
            # Specifically highlights: int, float, str, bool, list, dict, etc.
            (r'\b(print|int|float|str|bool|list|dict|set|tuple|range|len|type|sum|min|max)\b', "builtin")
        ]
    },
    "java": {
        "extensions": [".java"],
        "rules": [
            # Java Keywords (Blue)
            (r'\b(public|private|protected|static|final|transient|volatile|synchronized|native|instanceof|new|this|super|package|import|extends|implements|default)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(//.*$|/\*[\s\S]*?\*/)', "comment"),
            # Java Types (Gold/Orange)
            # Specifically includes primitives and standard library objects like String.
            (r'\b(int|double|float|long|short|byte|char|boolean|void|String|Integer|Double|Float|Boolean|var)\b', "type")
        ]
    },
    "c": {
        "extensions": [".c"],
        "rules": [
            (r'\b(int|char|float|double|void|volatile|static|extern|register|auto|struct|union|typedef|sizeof)\b', "type"),
            (r'\b(if|else|while|for|switch|case|break|continue|return|default|goto)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(//.*$|/\*[\s\S]*?\*/)', "comment"),
            (r'(#.*)', "preprocessor")
        ]
    },
    "cpp": {
        "extensions": [".cpp", ".h", ".hpp", ".cc"],
        "rules": [
            (r'\b(int|char|float|double|void|volatile|static|extern|register|auto|struct|union|typedef|sizeof)\b', "type"),
            (r'\b(if|else|while|for|switch|case|break|continue|return|default|goto)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(//.*$|/\*[\s\S]*?\*/)', "comment"),
            (r'(#.*)', "preprocessor")
        ]
    },
    "cs": {
        "extensions": [".cs"],
        "rules": [
            (r'\b(public|private|protected|internal|static|readonly|var|dynamic|base|this|using|namespace|partial|extern)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(//.*$|/\*[\s\S]*?\*/)', "comment")
        ]
    },
    "javascript": {
        "extensions": [".js", ".mjs", ".ts"],
        "rules": [
            (r'\b(function|const|let|var|if|else|for|while|import|export|default|class|return|async|await)\b', "keyword"),
            (r'(\".*?\"|\'.*?\')', "string"),
            (r'(//.*$|/\*[\s\S]*?\*/)', "comment")
        ]
    },
    "web": {
        "extensions": [".html", ".css", ".scss"],
        "rules": [
            (r'<[^>]+>', "tag"),
            (r'(\"[^\"]*\"|\'[^\']*\')', "string"),
            (r'(#.*)', "comment")
        ]
    }
}

# Legacy alias for backwards compatibility with main_app.py
LANGUAGES = LANGUAGES
