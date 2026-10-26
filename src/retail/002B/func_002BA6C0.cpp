extern "C" void func_002BA6C0(unsigned long long **cursor, unsigned int first, int second)
{
    unsigned long long *output = *cursor;
    *output++ = second;
    *output++ = first;
    *cursor = output;
}
