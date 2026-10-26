extern "C" float D_0034E9A8 __attribute__((section(".data")));
extern "C" float func_001A56B0(void);
extern "C" void func_001D0B88(int enabled)
{
    if (enabled)
        D_0034E9A8 = func_001A56B0();
}
