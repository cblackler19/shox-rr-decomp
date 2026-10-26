struct __attribute__((packed, aligned(4))) Block_2238A0 {
    unsigned long long first;
    unsigned int second;
};
extern "C" void func_002238A0(void *destination, const Block_2238A0 *source)
{
    if (source)
        *(Block_2238A0 *)((char *)destination + 8) = *source;
}
