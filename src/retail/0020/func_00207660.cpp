struct __attribute__((packed, aligned(4))) Block_207660 {
    unsigned long long first;
    unsigned int second;
};
extern "C" void func_00207660(void *destination, const Block_207660 *source)
{
    if (source)
        *(Block_207660 *)((char *)destination + 8) = *source;
}
