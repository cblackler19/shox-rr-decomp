extern "C" void func_00158DF8(unsigned int* destination, const unsigned int* source)
{
    unsigned int index = source[0];
    if (source[4] == 0) {
        unsigned int* item = destination + index;
        item[2] = 1;
    }
}
