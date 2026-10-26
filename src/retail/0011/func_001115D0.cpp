struct State_49B808 {
    void *first;
    void *second;
    unsigned int reserved[2];
};
extern "C" void func_00110850();
extern "C" void func_001115D0(State_49B808 *state)
{
    if (state->reserved[1])
        func_00110850();
}
