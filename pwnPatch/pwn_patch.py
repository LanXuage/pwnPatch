#!/bin/env python
# -*-coding:utf-8-*-
# author: LanXuage
# datetime: 2019-09-23
import os
import sys
import struct
import argparse

output = None
prog = sys.argv[0]


def hex_find(find_hex_values, data):
    res = []
    pos = -1
    while True:
        pre = pos + 1
        pos = data[pre:].find(find_hex_values)
        if pos == -1:
            break
        pos += pre
        pre_str = data[pos - 5: pos]
        aft_str = data[pos + len(find_hex_values): pos + len(find_hex_values) + 5]
        try:
            res.append({
                'pos': pos,
                'pre': ' '.join(['%02x' % ord(b) for b in pre_str]),
                'pre_str': pre_str,
                'aft': ' '.join(['%02x' % ord(b) for b in aft_str]),
                'aft_str': aft_str
            })
        except:
            res.append({
                'pos': pos,
                'pre': ' '.join(['%02x' % b for b in pre_str]),
                'pre_str': pre_str,
                'aft': ' '.join(['%02x' % b for b in aft_str]),
                'aft_str': aft_str
            })
    return res


def get_hex(one, two):
    find_hex_values = b''
    if one:
        if two:
            print("{}: error: Can't use -f/-r and -fs/-rs at the same time!".format(prog))
            return
        else:
            for fi in one:
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
                elif ' ' in fi:
                    for ffi in fi.split(' '):
                        ffi = ffi.strip()
                        if not ffi:
                            continue
                        find_hex_values += struct.pack('B', int(ffi, 16))
                else:
                    print('{}: error: -f(find)/-r(replace): The length of the value looked up is incorrect. \nPlease check it.'.format(prog))
                    return
    else:
        if two:
            for fi in two:
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
                elif ' ' in fi:
                    for ffi in fi.split(' '):
                        ffi = ffi.strip()
                        if not ffi:
                            continue
                        find_hex_values = struct.pack('B', int(ffi, 16)) + find_hex_values
                else:
                    print('{}: error: -f(find)/-r(replace): The length of the value looked up is incorrect. \nPlease check it.'.format(prog))
                    return
    return find_hex_values

def do_replace(find_hex_values, replace_hex_values, data):
    res = None
    return res

def hex_replace(find_hex_values, replace_hex_values, data):
    if len(find_hex_values) != len(replace_hex_values):
        try:
            is_go = str(raw_input('warning: Data length is different before and after replacement. \nDo you want to continue?(yes/no):')).strip()
        except NameError:
            is_go = str(input('warning: Data length is different before and after replacement. \nDo you want to continue?(yes/no):')).strip()
        if is_go.startswith('y') or is_go.startswith('Y'):
            res = do_replace(find_hex_values, replace_hex_values, data)
        else:
            print('Nothing be changed.')
    else:
        res = do_replace(find_hex_values, replace_hex_values, data)
    return res

def main():
    parser = argparse.ArgumentParser(prog=prog, description='A tool that can help you patch pwn or modify binary file is good!')
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
        find_hex_values = get_hex(args.f, args.fs)
        replace_hex_values = get_hex(args.r, args.rs)
        print(find_hex_values)#--
        print(replace_hex_values)#--
        if replace_hex_values == None or find_hex_values == None:
            return
        if find_hex_values != b'':
            find_res = hex_find(find_hex_values, data)
            print(find_res)
            if replace_hex_values != b'':
                hex_replace(find_hex_values, replace_hex_values, data)

        # output a new file.
        print(output)
        if output:
            if args.o:
                if os.path.exists(args.o):
                    try:
                        is_go = str(raw_input('warning: -o(output): file {} exists. \nContinuation will overwrite the original file. \nDo you want to continue?(yes/no):'.format(args.o))).strip()
                    except NameError:
                        is_go = str(input('warning: -o(output): file {} exists. \nContinuation will overwrite the original file. \nDo you want to continue?(yes/no):'.format(args.o))).strip()
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
            else:
                print(data)
            

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('User interrupts process.')
    except Exception as e:
        print('{}: error: {}'.format(prog, e))