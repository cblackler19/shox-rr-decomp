struct State_17F3E0 {
    int reserved;
    int *values;
};
extern "C" void func_00182088(int);
extern "C" void func_0017F3E0(State_17F3E0 *state, unsigned int index)
{
    int *value = state->values + index;
    func_00182088(*(int *)((char *)value + 76));
}
