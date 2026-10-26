struct GlobalFlag
{
    int value;
    unsigned int unused[2];
};

extern "C" GlobalFlag D_002DFC40;
extern "C" char D_0049B8E8[16];

extern "C" char* func_00118128()
{
    if (!D_002DFC40.value)
        D_002DFC40.value = 1;
    return D_0049B8E8;
}
