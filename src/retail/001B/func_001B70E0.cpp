struct State_1B70E0 {
    unsigned char unused[444];
    int mode;
    unsigned char gap[32];
    unsigned char bytes[3];
};
extern "C" void func_001B70E0(State_1B70E0 *state, unsigned int value)
{
    if (state->mode == 3) {
        state->bytes[1] = (unsigned char)(value >> 8);
        state->bytes[0] = (unsigned char)value;
        state->bytes[2] = (unsigned char)(value >> 16);
    }
}
