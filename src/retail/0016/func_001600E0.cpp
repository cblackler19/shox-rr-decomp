extern "C" int func_001600E0(int* state, const int* value)
{
    int previous = state[2];
    state[3] = previous;
    int current = value[0];
    int difference = current - previous;
    state[2] = current;
    state[4] = difference;
    return difference;
}