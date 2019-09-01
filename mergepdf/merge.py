import sys
import os
import os.path as path

from PyPDF2 import PdfFileMerger


def assert_files_exist(files):
    for f in files:
        if not path.isfile(f):
            print("Error:", f, "does not exist")
            sys.exit(-1)


def merge_files(input_files, output):
    assert_files_exist(input_files)
    merger = PdfFileMerger()
    for f in input_files:
        merger.append(f)
    merger.write(output)

def main(args):
    if len(args) < 3:
        print("Error: Must pass pdf files to merge.\nA minimum of two files must be passed in followed by the output file path")
        return -1

    merge_files(args[:-1], args[-1])



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
