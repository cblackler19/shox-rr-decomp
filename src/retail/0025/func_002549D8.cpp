extern "C" int D_00466A50 __attribute__((section(".data")));
extern "C" int D_0040C9B4 __attribute__((section(".data")));
extern "C" void func_002549D8(int flag, unsigned int value)
{
    if (value == 0xFFFF && flag)
        D_0040C9B4 = (int)&D_00466A50;
}
