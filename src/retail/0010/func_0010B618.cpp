extern "C" int func_0010B618(const int* base, unsigned int index)
{
    if (index >= 0x39)
        index = 0;
    const int* selected = base + index;
    return selected[6];
}