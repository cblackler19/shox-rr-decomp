extern "C" int func_002494B8(void *base, int offset)
{
    signed char *entry = (signed char *)base + offset;
    return entry[23] == 2 && *(int *)base != 0;
}
