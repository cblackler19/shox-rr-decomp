extern "C" void func_001A6050();

extern "C" void func_001AA0C0(void*, unsigned int flags)
{
    if (flags & 1)
        func_001A6050();
}
