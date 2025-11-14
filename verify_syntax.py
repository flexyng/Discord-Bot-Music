import ast
import sys

files = ['config.py', 'db.py', 'utils.py', 'cogs/owner.py', 'cogs/premium.py']

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f"[OK] {file} - Syntax OK")
    except SyntaxError as e:
        print(f"[ERROR] {file} - Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {file} - Error: {e}")
        sys.exit(1)

print("\n[OK] All files verified successfully!")
