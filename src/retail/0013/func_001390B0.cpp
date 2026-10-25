extern "C" void func_001390B0(char* base, unsigned int index, int value)
{
    if (index < 4) {
        char* record = base + (index * 4);
        *(int*)(record + 0x24) = value;
    }
}