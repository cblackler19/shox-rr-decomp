extern "C" int D_004660A0 __attribute__((section(".data")));
extern "C" void func_00100100(void *, void *, int);
extern "C" void func_0024D5F8(void *state, int value)
{
    func_00100100((char *)state + 148, &D_004660A0, value);
}
