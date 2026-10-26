struct GlobalState {
    unsigned char unused[732];
    int value;
};
extern "C" GlobalState D_00430000;
extern "C" int func_002BC960(int);

extern "C" int func_002AAAC8()
{
    return func_002BC960(D_00430000.value);
}
