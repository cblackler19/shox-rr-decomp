extern "C" void* func_001181A8(char* object, int value, short halfword)
{
    *(short*)object = halfword;
    *(int*)(object + 4) = value;
    return object;
}