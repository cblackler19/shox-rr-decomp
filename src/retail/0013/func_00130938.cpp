struct DataBlock
{
    unsigned char unused[0x188EC];
    unsigned int values[1];
};

extern "C" DataBlock D_002E02A0;

extern "C" unsigned int func_00130938(unsigned int index)
{
    return D_002E02A0.values[index];
}
