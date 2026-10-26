extern "C" float D_00354964 __attribute__((section(".data")));
extern "C" float func_001A56B0(void);
extern "C" void func_002239E0(int enabled)
{
    if (enabled)
        D_00354964 = func_001A56B0();
}
