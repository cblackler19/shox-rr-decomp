struct State_24D6C0 {
    unsigned char unused[88];
    int field88;
    int field92;
    float source96;
    float destination100;
    unsigned char gap104[4];
    float source108;
    float destination112;
    unsigned char gap116[80];
    int field196;
    int field200;
};
extern "C" void func_0024D6C0(State_24D6C0 *state)
{
    float first = state->source96;
    float second = state->source108;
    state->field88 = -1;
    state->destination100 = first;
    state->destination112 = second;
    state->field92 = 0;
    state->field196 = 0;
    state->field200 = 0;
}
