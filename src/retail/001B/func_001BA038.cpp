extern "C" void func_001BA038(void *object)
{
    int *table = *(int **)((char *)object + 28);
    char *entry = (char *)table + (table[0] - 1) * 4;
    unsigned char *target = (unsigned char *)*(int *)(entry + 4);
    target[564] = 0;
}
