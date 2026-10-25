struct Entry_001037E0
{
    int key;
    int value;
};
extern "C" int func_001037E0(int key, Entry_001037E0* entries, unsigned int count)
{
    for (unsigned int i = 0; i < count; ++i)
    {
        if (entries[i].key == key)
            return entries[i].value;
    }
    return 0;
}
