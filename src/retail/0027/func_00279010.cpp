extern "C" char D_0046BB30[] __attribute__((section(".data")));
extern "C" void func_00271BA8(void *);
extern "C" void func_00279010(void *object)
{
    *(char **)object = D_0046BB30;
    func_00271BA8(object);
}
