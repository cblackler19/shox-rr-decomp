extern "C" float D_00354968 __attribute__((section(".data")));
extern "C" float func_001A56B0(void);
extern "C" void func_00223A08(int enabled)
{
    if (enabled)
        D_00354968 = func_001A56B0();
}
