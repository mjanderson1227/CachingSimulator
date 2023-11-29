from cache_builder import CacheBuilder

# Address Object to encapsulate cache address.
class Address:
    full: int
    tag: int
    index: int
    offset: int

    # If the address does not have proper zero padding, then this will not work.
    def __init__(self, address: int, builder: CacheBuilder):
        while address >= builder.physical_size:
            address -= builder.physical_size
        self.full = address
        self.partition(builder)

    # Partition the address to conform with the address and cache parameters. Coupling this with cache builder is unavoidable at this point.
    def partition(self, builder: CacheBuilder):
        # Discard "0b"
        binary_string = bin(self.full)[2:]

        # Pad the binary string with zeros so that it conforms to the physical address.
        if len(binary_string) <= builder.address_bits:
            diff = builder.address_bits - len(binary_string)
            binary_string = ('0' * diff) + binary_string

        # Partition the string into the tag, index, and offset.
        self.tag = int(binary_string[0:builder.tag_bits], 2)
        off_begin = builder.index_bits + builder.tag_bits
        self.index = int(binary_string[builder.tag_bits:off_begin], 2)
        self.offset = int(binary_string[off_begin:], 2)
