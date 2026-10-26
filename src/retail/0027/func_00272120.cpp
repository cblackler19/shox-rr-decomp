extern "C" int func_00272228(void *);
extern "C" void func_00272120(void *object)
{
    int result = func_00272228(object);
    *(short *)((char *)object + 90) = (short)result;
}
