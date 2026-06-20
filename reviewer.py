import ast
import ollama


def _static_analysis(code: str) -> list[str]:
    findings = []

    for i, line in enumerate(code.splitlines(), 1):
        if len(line) > 79:
            findings.append(
                f"Line {i}: line too long ({len(line)} chars, limit 79)"
            )

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(
                f"Line {node.lineno}: bare `except:` — catches SystemExit "
                f"and KeyboardInterrupt, use `except Exception:` instead"
            )

        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in ("eval", "exec"):
                findings.append(
                    f"Line {node.lineno}: `{func.id}()` executes arbitrary "
                    f"code — security risk"
                )

    return findings


def review_code(code: str) -> str:
    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"Error: not valid Python — {e}"

    findings = _static_analysis(code)
    if findings:
        static_context = (
            "Static analysis found the following issues:\n"
            + "\n".join(f"- {f}" for f in findings)
            + "\n\nNow do a deeper review covering what static analysis cannot catch:\n\n"
        )
    else:
        static_context = (
            "Static analysis: no issues detected (no bare excepts, no eval/exec, "
            "all lines within 79 chars).\n\n"
            "Now do a deeper review covering what static analysis cannot catch:\n\n"
        )

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": f"""{static_context}## 1. BUGS
Runtime errors, wrong logic. Line number + reason.

## 2. INDENTATION
Tabs vs spaces, inconsistent levels, wrong nesting, PEP 8 (4 spaces). Line number + issue.

## 3. COMPLEXITY
Rate: Low/Medium/High. Flag overly long or deeply nested blocks. Suggest decomposition.

## 4. READABILITY
Non-descriptive or non-snake_case names. Missing docstrings. Bad/missing comments.

## 5. PERFORMANCE
Inefficient loops, redundant calls, better builtins/data structures, I/O inside loops.

## 6. SECURITY
Hardcoded secrets. eval/exec/shell=True. Unsafe input handling.

## 7. STRUCTURE
Single responsibility violations. Repeated code. Bare excepts. Import order (stdlib > third-party > local).

## 8. FIXES
Before/after code snippet for every issue above.

Code:
{code}""",
                }
            ],
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error: could not reach Ollama — is it running? ({e})"
