import os

def split_sql_file(filename, content):
    """Split SQL file if it contains two semicolons"""
    if content.count(';') == 2:
        parts = content.split(';', 1)
        base = filename.replace('.sql', '')
        with open(f"{base}_a.sql", 'w') as fa:
            fa.write(parts[0] + ';')
        with open(f"{base}_b.sql", 'w') as fb:
            fb.write(parts[1])
        print(f"Split {filename} into {base}_a.sql and {base}_b.sql")
        return True
    return False

for file in os.listdir('.'):
    if file.endswith('.sql'):
        with open(file, 'r') as f:
            content = f.read()
        split_sql_file(file, content)
