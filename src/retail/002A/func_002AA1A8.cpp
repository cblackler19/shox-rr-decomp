extern "C" int func_002AA098(int, int, int, int, int, void (*)());
extern "C" void func_002A9508();

extern "C" int func_002AA1A8(int a, int b, int c, int d, int e)
{
    return func_002AA098(a, b, c, d, e, func_002A9508);
}
