extern "C" unsigned int func_00107A28(void* base, unsigned int index, void** out)
{
    if (index < 6) {
        unsigned int offset = 0x8A0;
        offset *= index;
        offset += 0x6AE0;
        char* element = (char*)base + offset;
        *out = element;
        return *(unsigned int*)(element + 0x888);
    }
    return 0;
}