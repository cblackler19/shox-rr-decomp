extern "C" int func_00105640(int* object, unsigned int index, int** output)
{
    if (index < 4)
    {
        int* entry = object;
        entry += index;
        if (entry[0x62C] != 0)
        {
            *output = reinterpret_cast<int*>(reinterpret_cast<char*>(object) + 0x15E0 + index * 0x60);
            return 1;
        }
    }
    return 0;
}