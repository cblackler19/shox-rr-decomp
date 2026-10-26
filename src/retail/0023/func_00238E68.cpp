extern "C" int func_002C02C8(void *);

extern "C" int func_00238E68(void *object)
{
    void *value = *(void **)object;
    return func_002C02C8(*(void **)((char *)value + 4));
}
