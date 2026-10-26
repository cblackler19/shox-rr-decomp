extern "C" void func_00291A70(unsigned char* object, unsigned char value)
{
    unsigned int index = *(unsigned int*)object;
    unsigned char* entry = object + index;
    entry[16] = value;
    *(unsigned int*)object = (*(unsigned int*)object + 1) & 0x3FF;
}
