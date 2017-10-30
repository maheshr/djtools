#!/usr/bin/env python
import sys
import os
import os.path
import re

__author__ = 'mahesh'


def remove_pn(name):
    dir_part = os.path.dirname(name)
    file_part = os.path.basename(name)

    replace = file_part.replace("_PN", "")
    return os.path.join(dir_part, replace)


def remove_afterpn(name):
    dir_part = os.path.dirname(name)
    file_part = os.path.basename(name)

    index = file_part.find("_PN")
    replace = file_part[:(index+3)] + ".mp3"
    return os.path.join(dir_part, replace)


r = re.compile('([\d\-]*\s)')


def remove_num(name):
    dir_part = os.path.dirname(name)
    file_part = os.path.basename(name)

    m = r.match(file_part)
    replace = file_part
    if m:
        replace = file_part[m.end(1):]
        print replace

    return os.path.join(dir_part, replace)


def remove_1mp3_helper(suffix, name):
    dir_part = os.path.dirname(name)
    file_part = os.path.basename(name)

    if file_part.endswith(suffix):
        replace = file_part.replace(suffix, '.mp3')
        check = os.path.join(dir_part, replace)
        if os.path.isfile(check):
            print 'delete %s' % file_part
            os.unlink(name)
        else:
            print 'rename %s to %s' % (name, check)
            os.rename(name, check)


def remove_1mp3(name):
    remove_1mp3_helper(' 1.mp3', name)
    remove_1mp3_helper(' 2.mp3', name)
    remove_1mp3_helper(' 3.mp3', name)

    return name
    # return os.path.join(dir_part, file_part)


def rename_files_in_dir(arg, action):
    for file_or_dir in os.listdir(arg):
        process_file_or_dir(os.path.join(arg, file_or_dir), action)


def rename_file(arg, action):
    replace = arg
    if action == 'pn':
        replace = remove_pn(arg)
    elif action == 'num':
        replace = remove_num(arg)
    elif action == '1mp3':
        replace = remove_1mp3(arg)
    elif action == 'afterpn':
        replace = remove_afterpn(arg)

    if replace != arg:
        if not os.path.isfile(replace):
            os.rename(arg, replace)
            print("%s => %s" % (arg, replace))
        else:
            print("Skipping %s => %s as it exists" % (arg, replace))


def process_file_or_dir(arg, action):
    """

    :rtype : bool indicating whether arg was a valid file or dir
    """
    arg = os.path.expanduser(arg)
    arg = os.path.abspath(arg)
    if os.path.isdir(arg):
        rename_files_in_dir(arg, action)
    elif os.path.isfile(arg):
        rename_file(arg, action)
    else:
        return False
    return True


def main(args, action):
    for arg in args:
        arg = os.path.expanduser(arg)
        arg = os.path.abspath(arg)
        if not process_file_or_dir(arg, action):
            print("Unrecognized file or dir arg")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:], 'pn'))
