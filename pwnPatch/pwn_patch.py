#!/bin/env python
# -*- coding:utf-8 -*-
# author: LanXuage
# datetime: 2019-09-23
import os
import struct
import argparse

output = None
prog = 'papw'

def hex_find(find_hex_values, data):
    res = data.find(find_hex_values)
    return res

def main():
    parser = argparse.ArgumentParser(prog='papw', description='A tool that can help you patch pwn or modify binary file is good!')
    parser.add_argument('file', metavar='file', type=str, help='A executable file.')
    parser.add_argument('-f', metavar='find', type=str, nargs='+', help='Hex value to look for.')
    parser.add_argument('-fs', metavar='findSmallEnd', type=str, nargs='+', help='Small end of hex value to look for.')
    parser.add_argument('-r', metavar='replace', type=str, nargs='+', help='Hex value to be replaced.')
    parser.add_argument('-rs', metavar='replaceSmallEnd', type=str, nargs='+', help='Small end of hex value to be replaced.')
    parser.add_argument('-o', metavar='ouput', type=str, help='Output to a new file.')
    parser.add_argument('-a', metavar='all', nargs='?' , default=True, help='Show all result.')
    parser.add_argument('-v', action='version', version='%(prog)s 0.1')
    
    args = parser.parse_args()
    if os.path.exists(args.file):
        print(args)#--
        f = open(args.file, 'rb')
        data = f.read()
        f.close()
        find_hex_values = b''
        if args.f:
            if args.fs:
                print("{}: error: Can't use -f and -fs at the same time!".format(prog))
                return
            else:
                for fi in args.f:
                    if len(fi) == 2:
                            find_hex_values += struct.pack('B', int(fi, 16))
                    elif len(fi) % 3 == 0 and fi.startswith(r'x'):
                        for ffi in fi.split(r'x'):
                            ffi = ffi.strip()
                            if not ffi:
                                continue
                            find_hex_values += struct.pack('B', int(ffi, 16))
                    elif len(fi) & 1 == 0:
                        if fi.startswith(r'\x'):
                            for ffi in fi.split(r'\x'):
                                ffi = ffi.strip()
                                if not ffi:
                                    continue
                                find_hex_values += struct.pack('B', int(ffi, 16))
                        else:
                            try:
                                find_hex_values += bytes.fromhex(fi)
                            except AttributeError:
                                find_hex_values += fi.decode('hex')
                    else:
                        print('{}: error: -f(find): The length of the value looked up is incorrect. \nPlease check it.'.format(prog))
                        return
        else:
            if args.fs:
                for fi in args.fs:
                    if len(fi) == 2:
                            find_hex_values = struct.pack('B', int(fi, 16)) + find_hex_values
                    elif len(fi) % 3 == 0 and fi.startswith(r'x'):
                        for ffi in fi.split(r'x'):
                            ffi = ffi.strip()
                            if not ffi:
                                continue
                            find_hex_values = struct.pack('B', int(ffi, 16)) + find_hex_values
                    elif len(fi) & 1 == 0:
                        if fi.startswith(r'\x'):
                            for ffi in fi.split(r'\x'):
                                ffi = ffi.strip()
                                if not ffi:
                                    continue
                                find_hex_values = struct.pack('B', int(ffi, 16)) + find_hex_values
                        else:
                            try:
                                find_hex_values = bytes.fromhex(fi)[::-1] + find_hex_values
                            except AttributeError:
                                find_hex_values = fi.decode('hex')[::-1] + find_hex_values
                    else:
                        print('{}: error: -f(find): The length of the value looked up is incorrect. \nPlease check it.'.format(prog))
                        return

        print(find_hex_values)#--
        print(hex_find(find_hex_values, data))

        # output a new file.
        if args.o:
            if output:
                if os.path.exists(args.o):
                    try:
                        is_go=str(raw_input('warning: -o(output): file {} exists. \nContinuation will overwrite the original file. \nDo you want to continue?(yes/no):'.format(args.o))).strip()
                    except NameError:
                        is_go=str(input('warning: -o(output): file {} exists. \nContinuation will overwrite the original file. \nDo you want to continue?(yes/no):'.format(args.o))).strip()
                    if is_go.startswith('y') or is_go.startswith('Y'):
                        f = open(args.o, 'wb')
                        f.write(output)
                        f.close()
                        print('success.')
                    else:
                        print('Nothing be changed.')
                else:
                    f = open(args.o, 'wb')
                    f.write(output)
                    f.close()
            

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('User interrupts process.')
    except Exception as e:
        print('{}: error: {}'.format(prog, e))