import os
import sys
path = os.path.abspath(os.path.dirname(sys.argv[0]))

diff = []
details = False
with open("comparison_result.txt") as f:
    for line in f:
        line = line.strip().split(' ', 2)
        if len(line) >= 3:
            line[2] = line[2].strip()
            diff.append(line)
diff.sort(key=lambda x: x[2])
if details:
    for entry in diff:
        print(entry)

files_changed = []
files_deleted = []
files_added = []
last_item = None
for i, entry in enumerate(diff):
    if last_item is not None and entry[2] == last_item[2]:
        continue
    if i + 1 < len(diff) and diff[i+1][2] == entry[2]:
        # changed
        if diff[i+1][1] == entry[1]:
            print(f"Weird: MD5 are the same: {entry[2]}")
        files_changed.append(entry[2])
    else:
        if "<" in entry[0]:
            files_deleted.append(entry[2])
        elif ">" in entry[0]:
            files_added.append(entry[2])
        else:
            print(f"Weird: change sign unknown: {entry[0]}")
    last_item = entry
if details:
    print("---changed---")
    for entry in files_changed:
        print(entry)
    print("---added---")
    for entry in files_added:
        print(entry)
    print("---deleted---")
    for entry in files_deleted:
        print(entry)
# Save to file
files_to_zip = files_changed + files_added
with open('files_to_zip.txt', 'w') as f:
    for item in files_to_zip:
        f.write("%s\n" % item)
with open('files_to_delete.txt', 'w') as f:
    for item in files_deleted:
        f.write("%s\n" % item)
print("Files created.")
