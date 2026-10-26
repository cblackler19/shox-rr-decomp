extern "C" void func_001A6050();

extern "C" void func_001D0E48(void*, unsigned int flags)
{
    if (flags & 1)
        func_001A6050();
}
