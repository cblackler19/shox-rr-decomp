extern "C" void func_001B72E8(void);
extern "C" void func_001B7A08(void *unused, const unsigned int *value)
{
    if (*value == 0xF0DE)
        func_001B72E8();
}
