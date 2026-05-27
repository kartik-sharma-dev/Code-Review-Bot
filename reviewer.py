import ollama

def _is_python(code):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": f"""Is the following code written in Python?
Reply with ONLY one word: YES or NO. No explanation.

Code:
{code}"""
            }
        ]
    )
    answer = response["message"]["content"].strip().upper()
    return answer.startswith("YES")

def review_code(code):
    if not _is_python(code):
        return "❌ Error: Only Python code is accepted for review. Please submit valid Python code."

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": f"""Review this Python code. Be specific with line numbers. No vague feedback.

## 1. BUGS
Runtime errors, wrong logic. Line number + reason.

## 2. INDENTATION
Tabs vs spaces, inconsistent levels, wrong nesting, PEP 8 (4 spaces). Line number + issue.

## 3. COMPLEXITY
Rate: Low/Medium/High. Flag overly long or deeply nested blocks. Suggest decomposition.

## 4. READABILITY
Non-descriptive or non-snake_case names. Missing docstrings. Lines >79 chars. Bad/missing comments.

## 5. PERFORMANCE
Inefficient loops, redundant calls, better builtins/data structures, I/O inside loops.

## 6. SECURITY
Hardcoded secrets. eval/exec/shell=True. Unsafe input handling.

## 7. STRUCTURE
Single responsibility violations. Repeated code. Bare excepts. Import order (stdlib > third-party > local).

## 8. FIXES
Before/after code snippet for every issue above.

Code:
{code}"""
            }
        ]
    )
    return response["message"]["content"]
