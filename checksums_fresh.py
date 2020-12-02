import os
import hashlib
import shutil
used_disk_space = shutil.disk_usage("/").used
folder = "/"
output = "checksums_fresh.md5"
errors = "checksums_fresh_errors.log"
files_to_ignore = [output, errors, "checksums_final.md5", "checksums_final_errors.log", "checksums_fresh.py", "checksums_final.py"]
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
total = 0
successfully_scanned = 0
all_files_count = 0
print("Calculate total file count...")
try:
    for root, dirs, files in os.walk(folder):
        all_files_count += len(files)
except:
    pass
try:
    print("Scan started, please wait ...")
    with open(output, "w") as md5_list:
        with open(errors, "w") as error_list:
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    try:
                        if filename in files_to_ignore:
                            total += 1
                            continue
                        file_to_scan = os.path.join(root, filename)
                        #print(file_to_scan)
                        if not (os.path.isfile(file_to_scan) and not os.path.islink(file_to_scan)):
                            raise FileExistsError(f"File not found : {file_to_scan}")

                        file_size = os.path.getsize(file_to_scan)
                        if file_size > used_disk_space:
                            raise ValueError(f"Abnormal filesize of file: {file_to_scan}. Filesize {file_size/1024/1024}Mb larger than used disk space {used_disk_space/1024/1024}Mb")
                        md5_hash = ""
                        if file_size == 0:
                            md5_hash = "d41d8cd98f00b204e9800998ecf8427e"
                        else:
                            md5_hash = md5(file_to_scan)
                        md5_list.write(md5_hash + "  " + file_to_scan + "\n")
                        successfully_scanned += 1
                    except Exception as e:
                        error_list.write(str(e) +": " + filename + "\n")
                    finally:
                        total += 1
                    if total % 10000 == 0 and total != 0:
                        print(f"{round(total/all_files_count*100, 1)}% done: {total} out of {all_files_count} files scanned... (successfull: {successfully_scanned} - skipped: {total - successfully_scanned})")

    print(f"Scan finished: {successfully_scanned} files added. {total-successfully_scanned} files skipped (check {errors} for details)")
except Exception as e:
    print(f"Scan failed: {e}")
