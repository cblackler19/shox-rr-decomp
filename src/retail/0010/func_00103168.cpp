extern "C" unsigned char D_00446788[];

struct State {
    unsigned char padding0[0x14];
    unsigned int mask;
    unsigned int field18;
    unsigned char padding1[0x24 - 0x1C];
    unsigned int field24;
    unsigned char padding2[0x38 - 0x28];
    const void* table;
};

extern "C" State* func_00103168(State* state, unsigned int shift) {
    state->table = D_00446788;
    state->mask = (1U << shift) - 1U;
    state->field18 = 0;
    state->field24 = 0;
    return state;
}
