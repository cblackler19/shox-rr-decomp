struct __attribute__((packed)) SourceWord {
    unsigned long long value;
};
struct __attribute__((packed)) DestinationWord {
    unsigned char prefix[8];
    unsigned long long value;
};

extern "C" void func_001CCA98(void *dst, const void *src) {
    ((DestinationWord *)dst)->value = ((const SourceWord *)src)->value;
}
