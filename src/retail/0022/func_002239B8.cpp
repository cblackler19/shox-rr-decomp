extern "C" float D_00354960 __attribute__((section(".data")));
extern "C" float func_001A56B0(void);
extern "C" void func_002239B8(int enabled)
{
    if (enabled)
        D_00354960 = func_001A56B0();
}
