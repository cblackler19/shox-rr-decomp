struct Destination {
    unsigned char reserved[8];
    int value;
};
struct Source {
    unsigned int flags;
};

extern "C" void func_00125D80(Destination *destination, const Source *source) {
    if (source->flags & 0x10) {
        destination->value = 1;
    }
}
