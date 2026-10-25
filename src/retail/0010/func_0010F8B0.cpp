extern "C" unsigned int func_0010F8B0(void* object)
{
    unsigned int* counter = (unsigned int*)((char*)object + 0x80);
    unsigned int value = *counter + 1;
    *counter = value;
    value %= 3;
    *counter = value;
    return value;
}
