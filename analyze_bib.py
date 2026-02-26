import re

with open('proxyfailure.bib', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.split('\n@')
for entry in entries:
    entry_lower = entry.lower()
    if 'bregman' in entry_lower or 'wegner' in entry_lower or 'dalrymple' in entry_lower or 'frey' in entry_lower or 'levin1988' in entry_lower:
        # Extract title and author manually
        lines = entry.split('\n')
        key = lines[0].split('{')[-1].strip(',')
        print(f"KEY: {key}")
        for line in lines:
            if line.strip().lower().startswith('title') or line.strip().lower().startswith('author'):
                print(line.strip())
        print("---")
