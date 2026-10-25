extern "C" int func_00105680(int* object, unsigned int index, int** output)
{
    if (index < 4)
    {
        int* entry = object;
        entry += index;
        if (entry[0x630] != 0)
        {
            *output = reinterpret_cast<int*>(reinterpret_cast<char*>(object) + 0x1760 + index * 0x50);
            return 1;
        }
    }
    return 0;
}