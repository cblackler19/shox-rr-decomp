struct State_1A3A90 {
    int first;
    unsigned char flag4;
    unsigned char unused[511];
    unsigned char flag516;
    int field520;
    int field524;
    int padding528;
    int pointer532;
};
extern "C" int D_00458D00 __attribute__((section(".data")));
extern "C" State_1A3A90 *func_001A3A90(State_1A3A90 *state)
{
    state->first = 0;
    state->pointer532 = (int)&D_00458D00;
    state->flag516 = 0;
    state->field520 = 0;
    state->field524 = 0;
    state->flag4 = 0;
    return state;
}
