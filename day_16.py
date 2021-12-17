from io import StringIO, TextIOWrapper
from functools import partial, reduce
from operator import mul, gt, lt, eq


def handle_single_arg(f):
    def wrapper(*args):
        if len(args) == 2:
            return args[1]
        return f(*args)
    return wrapper

bin2int = partial(int, base=2)


class Packet:
    _type_id_map = {0: 'sum',
                    1: 'product',
                    2: 'min',
                    3: 'max',
                    4: 'get_literal_value',
                    5: gt,
                    6: lt,
                    7: eq}
    _len_type_id_map = {0: 'subpackets_by_length',
                        1: 'subpackets_by_number'}

    def __init__(self, fh):
        """
        >>> f = StringIO('38006F45291200')
        >>> p = Packet(f)
        >>> p.version
        1
        >>> p.type_id
        6
        >>> for s in p.subpackets:
        ...     print(s.literal_value)
        10
        20

        >>> f = StringIO('EE00D40C823060')
        >>> p = Packet(f)
        >>> p.version
        7
        >>> p.type_id
        3
        >>> p.len_type_id
        1
        >>> p.subpackets_count
        3
        >>> for s in p.subpackets:
        ...     print(s.literal_value)
        1
        2
        3
        """
        if isinstance(fh, (StringIO, TextIOWrapper)):
            self.buffer = "".join(map(lambda c: "{:04b}".format(int(c, base=16)), fh.read()))
        elif isinstance(fh, str):
            self.buffer = fh
        else:
            raise NotImplementedError
        self.version = bin2int(self.read(3))
        self.type_id = bin2int(self.read(3))
        self.len_type_id = None
        self.subpackets = []
        self.subpackets_bit_len = None
        self.subpackets_count = None
        self.literal_value = None

        func = self._type_id_map.get(self.type_id)
        if isinstance(func, str):
            func = getattr(self, func)
        self.func = func

        if func == self.get_literal_value:
            self.decode_literal_value()
        else:
            self.decode_subpackets()

    def read(self, bits):
        readval, self.buffer = self.buffer[:bits], self.buffer[bits:]
        return readval

    def decode_subpackets(self):
        self.len_type_id = bin2int(self.read(1))
        getattr(self, self._len_type_id_map.get(self.len_type_id))()

    def subpackets_by_length(self):
        self.subpackets_bit_len = bin2int(self.read(15))
        raw_subpackets = self.read(self.subpackets_bit_len)
        while raw_subpackets:
            p = Packet(raw_subpackets)
            raw_subpackets = p.buffer
            self.subpackets.append(p)

    def subpackets_by_number(self):
        self.subpackets_count = bin2int(self.read(11))
        raw_subpackets = self.buffer
        for _ in range(self.subpackets_count):
            p = Packet(raw_subpackets)
            raw_subpackets = p.buffer
            self.subpackets.append(p)
        self.buffer = raw_subpackets

    def decode_literal_value(self, *args):
        """
        >>> f = StringIO('D2FE28')
        >>> Packet(f).literal_value
        2021
        """
        bin_val = 0
        while True:
            raw = self.read(5)
            last_group_bit, value = map(bin2int, (raw[0], raw[1:]))
            bin_val = (bin_val << 4) + value
            if last_group_bit == 0:
                break
        self.literal_value = bin_val

    def get_literal_value(self):
        return self.literal_value

    @handle_single_arg
    def sum(self, *args):
        return sum(args)

    @handle_single_arg
    def product(self, *args):
        return reduce(mul, args)

    @handle_single_arg
    def min(self, *args):
        return min(args)

    @handle_single_arg
    def max(self, *args):
        return max(args)

    def eval(self):
        """
        >>> f = StringIO('C200B40A82')
        >>> Packet(f).eval()
        3
        >>> f = StringIO('04005AC33890')
        >>> Packet(f).eval()
        54
        >>> f = StringIO('880086C3E88112')
        >>> Packet(f).eval()
        7
        >>> f = StringIO('CE00C43D881120')
        >>> Packet(f).eval()
        9
        >>> f = StringIO('D8005AC2A8F0')
        >>> Packet(f).eval()
        1
        >>> f = StringIO('F600BC2D8F')
        >>> Packet(f).eval()
        0
        >>> f = StringIO('9C005AC2F8F0')
        >>> Packet(f).eval()
        0
        >>> f = StringIO('9C0141080250320F1802104A08')
        >>> Packet(f).eval()
        1
        """
        args = []
        for s in self.subpackets:
            args.append(s.eval())
        return self.func(*args)


def sum_packet_versions(p):
    """
    >>> f = StringIO('8A004A801A8002F478')
    >>> sum_packet_versions(Packet(f))
    16
    >>> f = StringIO('620080001611562C8802118E34')
    >>> sum_packet_versions(Packet(f))
    12
    >>> f = StringIO('C0015000016115A2E0802F182340')
    >>> sum_packet_versions(Packet(f))
    23
    >>> f = StringIO('A0016C880162017C3686B18A3D4780')
    >>> sum_packet_versions(Packet(f))
    31
    """
    total = p.version
    for s in p.subpackets:
        total += sum_packet_versions(s)
    return total


if __name__ == '__main__':
    with open('./input/day_16.txt', 'r') as f:
        p = Packet(f)
        print(f'part 1: {sum_packet_versions(p)}')

        f.seek(0)
        print(f'part 2: {Packet(f).eval()}')
