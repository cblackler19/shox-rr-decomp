extern "C" void func_001D0008(unsigned char *object, const unsigned int *index)
{
    unsigned int value = *index;
    if (value < 6)
        *(object + value + 8) = 1;
}
