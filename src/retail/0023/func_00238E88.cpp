extern "C" int func_002C0538(void *);

extern "C" int func_00238E88(void *object)
{
    void *value = *(void **)object;
    return func_002C0538(*(void **)((char *)value + 4));
}
