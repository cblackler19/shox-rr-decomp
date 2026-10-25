struct State {
    unsigned char padding[0x68];
    unsigned int value;
};

extern "C" void func_00112E60(State* state) {
    state->value = 0xFFFFFFFF;
}
