extern "C" unsigned int func_002B9B48(unsigned int value)
{
    if ((value >> 28) == 7) {
        value &= 0x0fffffff;
        value |= 0x80000000;
    }
    return value;
}
