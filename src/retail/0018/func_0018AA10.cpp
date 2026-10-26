struct ValueCell
{
    unsigned int value;
    unsigned int unused[2];
};

extern "C" ValueCell D_0032A7B0;
extern "C" void func_0018BB20(unsigned int);

extern "C" void func_0018AA10()
{
    func_0018BB20(D_0032A7B0.value);
}
