extern "C" int func_0027D090(const unsigned int* object)
{
    unsigned int flags = object[1];
    if (flags & 0x10u)
        return 0;
    return (flags & 0xFu) == 0;
}
