extern "C" void func_001A6050();

extern "C" void func_001ABA70(void*, unsigned int flags)
{
    if (flags & 1)
        func_001A6050();
}
