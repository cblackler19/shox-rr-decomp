extern "C" float D_0045BB44 __attribute__((section(".data")));
extern "C" float D_0034E9C8 __attribute__((section(".data")));
extern "C" void func_001D1B50(int flag, unsigned int value)
{
    if (value == 0xFFFF && flag)
        D_0034E9C8 = D_0045BB44;
}
