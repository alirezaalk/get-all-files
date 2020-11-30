#!/bin/bash
rm changes.tar.gz
tar cvzf changes.tar.gz -T files_to_zip.txt --ignore-failed-read  > zip_compared_stdout.log 2> zip_compared_stderr.log
