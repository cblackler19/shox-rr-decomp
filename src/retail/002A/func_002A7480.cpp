struct FunctionTable {
    unsigned char unused[304];
    int (*callback)();
};
extern "C" FunctionTable D_00430000;

extern "C" int func_002A7480()
{
    return D_00430000.callback();
}
