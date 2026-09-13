"""A minimal animated-GIF writer, because no image library is installed here.

Writes GIF89a with a global colour table, the Netscape looping extension, and
LZW-compressed frames. Only what this project needs: one palette for the whole
animation, full-frame updates, no interlacing, no transparency.
"""

import struct


class _Bits:
    """LSB-first bit packer, emitted as GIF data sub-blocks."""

    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.nbits = 0

    def write(self, code, size):
        self.acc |= code << self.nbits
        self.nbits += size
        while self.nbits >= 8:
            self.out.append(self.acc & 0xFF)
            self.acc >>= 8
            self.nbits -= 8

    def flush(self):
        if self.nbits:
            self.out.append(self.acc & 0xFF)
            self.acc = 0
            self.nbits = 0
        return bytes(self.out)


def lzw_encode(data, min_code_size):
    """GIF-flavoured LZW. ``data`` is a bytes-like of palette indices."""
    clear = 1 << min_code_size
    eoi = clear + 1
    bits = _Bits()
    code_size = min_code_size + 1
    table = {bytes([i]): i for i in range(clear)}
    next_code = eoi + 1
    bits.write(clear, code_size)
    if not data:
        bits.write(eoi, code_size)
        return bits.flush()
    cur = bytes([data[0]])
    for byte in data[1:]:
        nxt = cur + bytes([byte])
        if nxt in table:
            cur = nxt
            continue
        bits.write(table[cur], code_size)
        if next_code < 4096:
            table[nxt] = next_code
            next_code += 1
            if next_code > (1 << code_size) and code_size < 12:
                code_size += 1
        else:
            bits.write(clear, code_size)
            table = {bytes([i]): i for i in range(clear)}
            next_code = eoi + 1
            code_size = min_code_size + 1
        cur = bytes([byte])
    bits.write(table[cur], code_size)
    bits.write(eoi, code_size)
    return bits.flush()


def _sub_blocks(payload):
    out = bytearray()
    for i in range(0, len(payload), 255):
        chunk = payload[i : i + 255]
        out.append(len(chunk))
        out += chunk
    out.append(0)
    return bytes(out)


def _table_bits(n_colors):
    bits = 1
    while (1 << bits) < n_colors:
        bits += 1
    return max(1, bits)


def write_gif(path, frames, palette, width, height, delays_cs, loop=0):
    """Write an animated GIF.

    ``frames``   list of bytes-like, each ``width * height`` palette indices
    ``palette``  list of ``(r, g, b)``, at most 256 entries
    ``delays_cs``int, or one int per frame, in hundredths of a second
    """
    if not frames:
        raise ValueError("no frames")
    if len(palette) > 256:
        raise ValueError("palette has more than 256 entries")
    if isinstance(delays_cs, int):
        delays_cs = [delays_cs] * len(frames)
    if len(delays_cs) != len(frames):
        raise ValueError("delays must match frame count")
    for f in frames:
        if len(f) != width * height:
            raise ValueError("frame size does not match width * height")

    bits = _table_bits(len(palette))
    table_size = 1 << bits
    out = bytearray(b"GIF89a")
    out += struct.pack("<HH", width, height)
    out.append(0x80 | (bits - 1))  # global colour table, its size
    out += b"\x00\x00"  # background index, pixel aspect ratio
    for i in range(table_size):
        r, g, b = palette[i] if i < len(palette) else (0, 0, 0)
        out += bytes((r & 0xFF, g & 0xFF, b & 0xFF))

    out += b"\x21\xff\x0bNETSCAPE2.0\x03\x01" + struct.pack("<H", loop) + b"\x00"

    min_code_size = max(2, bits)
    for frame, delay in zip(frames, delays_cs):
        out += b"\x21\xf9\x04\x00" + struct.pack("<H", delay) + b"\x00\x00"
        out += b"\x2c" + struct.pack("<HHHH", 0, 0, width, height) + b"\x00"
        out.append(min_code_size)
        out += _sub_blocks(lzw_encode(bytes(frame), min_code_size))
    out.append(0x3B)

    with open(path, "wb") as fh:
        fh.write(out)
    return len(out)


def lzw_decode(payload, min_code_size):
    """Decoder used by the tests to check the encoder against itself."""
    clear = 1 << min_code_size
    eoi = clear + 1
    code_size = min_code_size + 1
    table = [bytes([i]) for i in range(clear)] + [b"", b""]
    out = bytearray()
    acc = nbits = 0
    prev = None
    pos = 0
    while True:
        while nbits < code_size:
            if pos >= len(payload):
                return bytes(out)
            acc |= payload[pos] << nbits
            nbits += 8
            pos += 1
        code = acc & ((1 << code_size) - 1)
        acc >>= code_size
        nbits -= code_size
        if code == clear:
            table = [bytes([i]) for i in range(clear)] + [b"", b""]
            code_size = min_code_size + 1
            prev = None
            continue
        if code == eoi:
            return bytes(out)
        if code < len(table):
            entry = table[code]
        elif prev is not None:
            entry = prev + prev[:1]
        else:
            raise ValueError("corrupt LZW stream")
        out += entry
        if prev is not None:
            table.append(prev + entry[:1])
            if len(table) > (1 << code_size) and code_size < 12:
                code_size += 1
        prev = entry


def read_sub_blocks(data, pos):
    """Concatenate GIF sub-blocks starting at ``pos``; returns (payload, next_pos)."""
    payload = bytearray()
    while True:
        n = data[pos]
        pos += 1
        if n == 0:
            return bytes(payload), pos
        payload += data[pos : pos + n]
        pos += n
