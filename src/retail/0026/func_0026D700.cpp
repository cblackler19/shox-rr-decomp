extern "C" int func_0026D700(void *base, unsigned char index, int value)
{
    if (index < 4) {
        unsigned char *entry = (unsigned char *)base + index;
        entry[316] = value;
        return 1;
    }
    return 0;
}
