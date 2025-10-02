import os
for root, dirs, files in os.walk("ts_app_deepseek"):
    level = root.replace("ts_app_deepseek", "").count(os.sep)
    indent = " " * 4 * (level)
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")
