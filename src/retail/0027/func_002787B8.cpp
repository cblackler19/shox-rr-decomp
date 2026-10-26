extern "C" void func_002787D8();

extern "C" void func_002787B8(void *record, int value)
{
    *(int *)record = value;
    func_002787D8();
}
