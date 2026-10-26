extern "C" void func_00288050(void *);
extern "C" void func_002A8248(void *object)
{
    void *child = *(void **)((char *)object + 28);
    if (child)
        func_00288050(child);
}
