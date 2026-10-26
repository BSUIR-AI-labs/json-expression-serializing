# JSON Expression Serializer

Parses arithmetic expressions into a hierarchical JSON and saves the result to `output.json`.

## Supported
- Operators: `+`, `-`, `*`, `/`, `^`, `=`
- Implicit multiplication: `ax` → `a*x`, `2(a+b)` → `2*(a+b)`
- Parentheses and unary minus
- Decimal numbers: `2.5`

## Run
```bash
python main.py