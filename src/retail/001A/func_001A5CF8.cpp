struct State_1A5CF8 {
    unsigned short index;
    unsigned char unused[18];
    int value20;
};
extern "C" void func_001A5CF8(State_1A5CF8 *state)
{
    if (state->index >= 3) {
        --state->index;
        *((unsigned char *)state + state->index + 3579) = 0;
    }
    state->value20 = 0;
}
