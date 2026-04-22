import os
import json

def get_dir_details(path='.'):
    data = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            stats = os.stat(file_path)
            data.append({
                "name": file,
                "path": file_path,
                "size_kb": stats.st_size / 1024,
                "modified": stats.st_mtime
            })
    return json.dumps(data, indent=4)

print(get_dir_details())