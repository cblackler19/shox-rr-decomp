extern "C" int D_00422298 __attribute__((section(".data")));
extern "C" int D_002DFC38 __attribute__((section(".data")));
extern "C" void func_00117B48(int flag, unsigned int value)
{
    if (value == 0xFFFF && flag)
        D_002DFC38 = D_00422298;
}
