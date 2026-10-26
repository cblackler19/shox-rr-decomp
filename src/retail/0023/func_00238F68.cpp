extern "C" int func_002BFF10(void *);

extern "C" int func_00238F68(void *object)
{
    void *value = *(void **)object;
    return func_002BFF10(*(void **)((char *)value + 4));
}
