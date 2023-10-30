import re
with open(r'Your_directory\4528.dmp', 'rb') as f:
    data = f.read().strip()


# pattern = rb'"createdTime":(.+)"text":("[\w\s:<]+)(")'
# pattern = rb'"createdTime":(.+)"text":(".+)(")'
pattern = rb'([\w\s\.,]+){"e2eeMark":'
regex = re.compile(pattern)

matches = regex.finditer(data)

if matches:
    for match in matches:
        # print("\n")
        print("Found:", match.group(1))
else:
    print("No matches found.")