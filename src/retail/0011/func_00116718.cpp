struct GlobalState
{
    unsigned int unused[2];
    float first;
    float fourth;
    float third;
    float second;
    unsigned int count;
};

extern "C" GlobalState D_0049B8C8;

extern "C" void func_00116718()
{
    register float zero = 0.0f;
    D_0049B8C8.count = 0;
    D_0049B8C8.second = zero;
    D_0049B8C8.third = zero;
    D_0049B8C8.fourth = zero;
    D_0049B8C8.first = zero;
}
