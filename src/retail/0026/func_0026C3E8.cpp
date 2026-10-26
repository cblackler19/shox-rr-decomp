extern "C" void func_0026C3E8(int **values, unsigned int index, int value)
{
    int *base = *values;
    if (index < 9)
        *(int *)((char *)base + (index << 2)) = value;
}
