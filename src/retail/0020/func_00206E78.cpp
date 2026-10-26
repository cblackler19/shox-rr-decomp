extern "C" float D_0045BB44 __attribute__((section(".data")));
extern "C" float D_0053BA48 __attribute__((section(".data")));
extern "C" void func_00206E78(int flag, unsigned int value)
{
    if (value == 0xFFFF && flag)
        D_0053BA48 = D_0045BB44;
}
