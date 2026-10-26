extern "C" void func_001BA498(unsigned int*);

extern "C" void func_001B9E18(unsigned int* object)
{
    object[3] = 0;
    func_001BA498(object + 21);
}
