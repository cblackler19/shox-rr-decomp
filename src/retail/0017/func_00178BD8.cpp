struct State_178BD8 {
    int field0;
    int field4;
    int field8;
    int field12;
    int field16;
    unsigned char unused[360];
    int mode;
};
extern "C" void func_00178BD8(State_178BD8 *state)
{
    int *fields = &state->field4;
    fields[3] = 0;
    if (state->mode == 1) {
        fields[1] = 0;
        fields[2] = 0;
    }
}
