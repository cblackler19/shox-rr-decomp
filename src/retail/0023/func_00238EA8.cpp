extern "C" int func_002C0090(void *);

extern "C" int func_00238EA8(void *object)
{
    void *value = *(void **)object;
    return func_002C0090(*(void **)((char *)value + 4));
}
