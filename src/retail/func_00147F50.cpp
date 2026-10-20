extern "C" int func_00147F50(const int* base, unsigned int index)
{
    if (index >= 4)
        index = 0;
    const int* selected = base + index;
    return selected[0x94];
}