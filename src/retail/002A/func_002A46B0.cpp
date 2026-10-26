extern "C" void func_002A74A8(void *);
extern "C" void func_002A46B0(void *object)
{
    void *child = *(void **)((char *)object + 28);
    if (child)
        func_002A74A8(child);
}
