import re
import json
import ast

files = [
    ("engines/autonomic.py", "quizzes/autonomic.json"),
    ("engines/nervemuscle.py", "quizzes/nervemuscle.json"),
]

for source, target in files:

    with open(source, "r", encoding="utf-8") as f:
        text = f.read()

    match = re.search(
        r"questions\s*=\s*(\[[\s\S]*?\])\s*\n\s*current_round",
        text
    )

    if not match:
        print(f"Could not parse {source}")
        continue

    questions = ast.literal_eval(match.group(1))

    with open(target, "w", encoding="utf-8") as f:
        json.dump(
            questions,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Created {target} with {len(questions)} questions"
    )
