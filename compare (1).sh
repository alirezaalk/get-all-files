#!/bin/bash
now=$(date +"%T")
echo "started: $now"
diff <(sort checksums_fresh.md5) <(sort checksums_final.md5) > comparison_result.txt
now=$(date +"%T")
echo "Diff done: $now"
python3 format_compared_files.py
now=$(date +"%T")
echo "format result done: $now"
