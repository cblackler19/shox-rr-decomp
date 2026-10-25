extern "C" void func_002865A8(int value, int index, int flags);
extern "C" void func_00112578(void* object)
{
    unsigned char* base = (unsigned char*)object;
    int current = *(int*)(base + 48);
    if (*(int*)(base + 52) != current) {
        int value = *(int*)(base + 80) - 1;
        int index = *(short*)(base + 48);
        *(int*)(base + 52) = current;
        func_002865A8(value, index, 0);
    }
}