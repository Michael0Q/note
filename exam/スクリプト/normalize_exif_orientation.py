#!/usr/bin/env python3
"""JPEGのEXIF orientationタグを1（回転不要）に書き換える。

sipsで回転補正した写真にはEXIFの向きタグが残ることがあり、
タグを解釈するビューア（Obsidian等）では二重に回転して表示される。
ピクセルを正立させたあと、このスクリプトでタグを無効化して統一する。

使い方: python3 normalize_exif_orientation.py <file.jpg> [file2.jpg ...]
"""
import struct, sys


def fix_orientation(path):
    with open(path, 'rb') as f:
        data = bytearray(f.read())
    if data[:2] != b'\xff\xd8':
        return 'not-jpeg'
    i = 2
    while i < len(data) - 4:
        if data[i] != 0xFF:
            break
        marker = data[i + 1]
        seglen = struct.unpack('>H', bytes(data[i + 2:i + 4]))[0]
        if marker == 0xE1 and data[i + 4:i + 10] == b'Exif\x00\x00':
            base = i + 10
            endian = '<' if data[base:base + 2] == b'II' else '>'
            ifd = struct.unpack(endian + 'I', bytes(data[base + 4:base + 8]))[0]
            n = struct.unpack(endian + 'H', bytes(data[base + ifd:base + ifd + 2]))[0]
            for k in range(n):
                e = base + ifd + 2 + k * 12
                tag = struct.unpack(endian + 'H', bytes(data[e:e + 2]))[0]
                if tag == 0x0112:
                    old = struct.unpack(endian + 'H', bytes(data[e + 8:e + 10]))[0]
                    if old == 1:
                        return 'already-1'
                    data[e + 8:e + 10] = struct.pack(endian + 'H', 1)
                    with open(path, 'wb') as f:
                        f.write(data)
                    return f'{old} -> 1'
            return 'no-orientation-tag'
        i += 2 + seglen
    return 'no-exif'


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, ':', fix_orientation(p))
