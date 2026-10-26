struct InitBlock {
    int value;
    int first;
    int second;
    int unused0[3];
    int third;
    int unused1;
    int fourth;
    int unused2;
    int fifth;
};

extern "C" InitBlock *func_00239AC0(InitBlock *block)
{
    block->first = 0;
    block->value = 16;
    block->second = 0;
    block->third = 0;
    block->fourth = 0;
    block->fifth = 0;
    return block;
}
