extern "C" int func_00288878(int, int);
extern "C" int func_00274900(void *object, int index)
{
    return func_00288878(*(int *)((char *)object + 12), index - 1) == 1;
}
