struct Entry {
    unsigned int pad[54];
    unsigned int index;
};

extern "C" int func_00275E40(int *base, Entry *entry)
{
    if (entry != 0)
        return *(int *)((char *)base + (entry->index << 2) + 336);
    return 0;
}
