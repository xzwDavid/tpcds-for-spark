import os
import re

def fix_sql(content):
    # 修复任何 xxxdays 的列名情况，将单引号改为双引号
    content = re.sub(r'as\s+\'(\w+days)\'', r'as "\1"', content)
    
    # 修复 interval X days 的加法情况
    def replace_interval_add(match):
        before_part = match.group(1)
        days = match.group(2)
        if 'date_add' in before_part:
            return match.group(0)
        return f"date_add('day', {days}, {before_part})"
    
    # 修复 interval X days 的减法情况
    def replace_interval_sub(match):
        before_part = match.group(1)
        days = match.group(2)
        if 'date_add' in before_part:
            return match.group(0)
        return f"date_add('day', -{days}, {before_part})"
    
    # 处理加法情况
    content = re.sub(r'((?:cast\s*\([^)]+\)|cast\s*\([^)]+\)\s+as\s+date))\s*\+\s*interval\s+(\d+)\s+days',
                    replace_interval_add, content)
    
    # 处理减法情况
    content = re.sub(r'((?:cast\s*\([^)]+\)|cast\s*\([^)]+\)\s+as\s+date))\s*-\s*interval\s+(\d+)\s+days',
                    replace_interval_sub, content)
    
    # 处理包含days且长度不为4的词
    def replace_days_word(match):
        word = match.group(1)
        if 'days' in word and len(word) != 4:
            return f'"{word}"'
        return word
    
    content = re.sub(r'\b(\w+days)\b', replace_days_word, content)
    
    # 修复所有形如 'YYYY-MM-DD' 的日期字符串，添加 cast
    def replace_date(match):
        before_quote = match.group(1)
        if 'cast(' in before_quote.split('\n')[-1]:
            return match.group(0)
        return f"{before_quote}cast('{match.group(2)}' as date)"
    
    # 修复between日期的情况
    def replace_between_date(match):
        before_between = match.group(1)
        date1 = match.group(2)
        date2 = match.group(3)
        if 'cast(' in before_between.split('\n')[-1]:
            return match.group(0)
        return f"{before_between}between cast('{date1}' as date) and cast('{date2}' as date)"
    
    # 先处理between的情况
    content = re.sub(r'(between\s+)\'(\d{4}-\d{1,2}-\d{1,2})\'\s+and\s+\'(\d{4}-\d{1,2}-\d{1,2})\'',
                    replace_between_date, content)
    
    # 再处理单独的日期
    content = re.sub(r'([^\'"\w])\'(\d{4}-\d{1,2}-\d{1,2})\'',
                    replace_date, content)
    
    return content

for file in os.listdir('.'):
    if file.endswith('.sql'):
        with open(file, 'r') as f:
            content = f.read()
            
        # 修复SQL语法
        fixed_content = fix_sql(content)
        
        # 如果有两个分号，则分割文件
        if fixed_content.count(';') == 2:
            parts = fixed_content.split(';', 1)
            base = file.replace('.sql', '')
            with open(f"{base}_a.sql", 'w') as fa:
                fa.write(parts[0] + ';')
            with open(f"{base}_b.sql", 'w') as fb:
                fb.write(parts[1])
            print(f"Split {file} into {base}_a.sql and {base}_b.sql")
        # 如果内容有修改但不需要分割，则更新原文件
        elif fixed_content != content:
            with open(file, 'w') as f:
                f.write(fixed_content)
            print(f"Fixed {file}")
