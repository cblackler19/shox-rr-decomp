extern "C" int func_001FC9A8(void *object)
{
    if (object)
    {
        unsigned int *field = (unsigned int *)((char *)object + 12);
        *field += (unsigned int)object;
        return 1;
    }
    return 0;
}
