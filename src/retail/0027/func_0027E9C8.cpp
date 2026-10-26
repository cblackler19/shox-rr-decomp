extern "C" int func_0027E9C8(unsigned int* destination, const unsigned int* source)
{
    unsigned int value;
    if (source[3] & 0x80u)
        value = source[2];
    else
        value = source[4];
    *destination = value;
    return 1;
}
