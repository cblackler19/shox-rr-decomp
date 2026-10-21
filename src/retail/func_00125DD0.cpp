struct StateAt8 { int unused[2]; int value; };
extern "C" void func_00125DD0(StateAt8* state, int* source) {
    if (*source == 2) {
        state->value = 1;
        return;
    }
    state->value = 0;
}
