extern "C" void func_00147F28(unsigned char* object, unsigned int index, int value)
{
    if (index < 4 && value < 3) {
        unsigned char* row = object + index * 4;
        *(unsigned int*)(row + 0x250) = (unsigned int)value;
    }
}
