extern "C" int func_001FA570(void *object, unsigned int index)
{
    int *values = *(int **)((char *)object + 8);
    return values[index & 0xffff];
}
