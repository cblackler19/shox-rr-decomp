extern "C" int func_002AA240(void *, int);
extern "C" int func_0026D0F0(void *object)
{
    void *child = *(void **)((char *)object + 4);
    return child ? func_002AA240(child, 100) : 0;
}
