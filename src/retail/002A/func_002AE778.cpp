struct Entry
{
    unsigned int unused[12];
    unsigned int value;
};

extern "C" Entry* D_004357F0[64];

extern "C" unsigned int func_002AE778(void*, unsigned int index)
{
    return D_004357F0[index & 0x3F]->value;
}
