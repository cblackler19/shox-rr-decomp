extern "C" int D_004222CC __attribute__((section(".data")));
extern "C" void func_0026C440(int, int);
extern "C" int func_0026EFB8(void *object)
{
    int value = *(int *)((char *)object + 4);
    func_0026C440(D_004222CC, value);
    return 1;
}
