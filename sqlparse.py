from sys import argv
import re

__author__ = 'thomas'

script, filename = argv

def delimited(file, delimiter='\n', bufsize=4096):
    buf = ''
    while True:
        newbuf = file.read(bufsize)
        if not newbuf:
            yield buf
            return
        buf += newbuf
        lines = buf.split(delimiter)
        for line in lines[:-1]:
            yield line
        buf = lines[-1]

pattern = r'\s*insert\s+into\s+(\w+)\s+\((.*)\).*\((.*)\)'
file = open(filename)
file2 = delimited(file, delimiter=';')

columnsToRemove = ('B', 'F')

for line in file2:
    line = line.replace('\n', '')
    match = re.match(pattern, line, re.IGNORECASE)
    table = match.group(1)
    names = [x.strip() for x in match.group(2).split(',')]
    values =[x.strip() for x in match.group(3).split(',')]
    cols = dict(zip(names, values))
    names = [x for x in names if x not in columnsToRemove]
    values = [cols[x] for x in names]
    statement = 'INSERT INTO {} ({}) VALUES ({});'.format(table, ', '.join(names), ','.join(values))
    print(statement)
