struct State_12C6B8 {
    unsigned char unused[152];
    int ready;
    int padding;
    int active;
};
extern "C" void func_0012C6E0(State_12C6B8 *);
extern "C" void func_0012C6B8(State_12C6B8 *state)
{
    state->active = 1;
    state->ready = 0;
    func_0012C6E0(state);
}
