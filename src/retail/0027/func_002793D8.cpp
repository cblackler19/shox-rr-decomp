extern "C" char D_0046B960[] __attribute__((section(".data")));
extern "C" void func_00271BA8(void *);
extern "C" void func_002793D8(void *object)
{
    *(char **)object = D_0046B960;
    func_00271BA8(object);
}
