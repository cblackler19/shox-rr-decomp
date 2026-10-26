extern "C" float func_001F2B10(void *object)
{
    char *base = *(char **)((char *)object + 8);
    int index = *(int *)base - 1;
    return *(float *)(base + index * 20 + 4);
}
