extern "C" int func_00277E30(const int *values, int index)
{
    if (index < 64)
        return *(const int *)((const char *)values + (index << 2));
    return 0;
}
