struct State_1ADD18 {
    unsigned char unused[264];
    int first;
    int second;
    int third;
};
extern "C" void func_001ACFF0(State_1ADD18 *);
extern "C" void func_001ADD18(State_1ADD18 *state)
{
    state->first = 0;
    state->second = 0;
    state->third = 0;
    func_001ACFF0(state);
}
