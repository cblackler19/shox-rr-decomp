extern "C" int func_0019FD40(unsigned char *base, unsigned int row, unsigned int column)
{
    row &= 0xFF;
    column = column * 2 + row * 102;
    unsigned short value = *(unsigned short *)(base + column + 2104);
    return value >= 4096;
}
