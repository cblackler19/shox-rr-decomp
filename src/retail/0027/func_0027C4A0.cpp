typedef int (*Method_0027C4A0)(char *);
extern "C" int func_0027C4A0(int, int, char *object)
{
    char *vtable = *(char **)(object + 104);
    short adjustment = *(short *)(vtable + 32);
    Method_0027C4A0 method = *(Method_0027C4A0 *)(vtable + 36);
    return method(object + adjustment);
}
