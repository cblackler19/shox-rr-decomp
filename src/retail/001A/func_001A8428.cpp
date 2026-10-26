extern "C" void func_001A8800(int, int *);

extern "C" void func_001A8428(int, int *value)
{
    if (value)
        func_001A8800(*value, value);
}
