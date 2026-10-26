struct __attribute__((packed)) PackedWord
{
    unsigned long long value;
};

extern "C" void func_001CCAD0(void *destination, const void *source)
{
    if (source)
        ((PackedWord *)((char *)destination + 8))->value = ((const PackedWord *)source)->value;
}
