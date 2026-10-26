struct FunctionTable {
    unsigned char unused[308];
    int (*callback)();
};
extern "C" FunctionTable D_00430000;

extern "C" int func_00297DA8()
{
    return D_00430000.callback();
}
