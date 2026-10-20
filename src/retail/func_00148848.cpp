extern "C" int func_00148848(const char* base, unsigned int index)
{
    if (index >= 4)
        index = 0;
    const char* selected = base + (index * 12);
    return *(const int*)(selected + 0x254) != 0;
}