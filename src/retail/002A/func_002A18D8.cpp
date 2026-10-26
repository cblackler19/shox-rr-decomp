struct GlobalState
{
    char pad[12];
    unsigned short count;
    char reserved[590];
    void (*callback)();
};

extern "C" GlobalState D_0042D978;
extern "C" void func_002A62C0();

extern "C" void func_002A18D8()
{
    D_0042D978.callback = func_002A62C0;
    D_0042D978.count = 1024;
}
