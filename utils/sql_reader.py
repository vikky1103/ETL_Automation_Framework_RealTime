import re


def load_queries(file_path):
    queries = {}
    content = open(file_path, encoding="utf-8").read()
    blocks = re.split(r"--\s*\[(.*?)\]", content)
    for i in range(1, len(blocks), 2):
        key = blocks[i].strip()
        query = blocks[i + 1].strip()
        if key and query:
            queries[key] = query
    return queries
