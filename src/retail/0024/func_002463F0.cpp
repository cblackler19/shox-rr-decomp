struct State_2463F0 { int reserved; int defaultIndex; };
extern "C" int func_002463F0(State_2463F0 *state, int index)
{
    int offset;
    if (index == -1)
        offset = state->defaultIndex * 704;
    else
        offset = index * 704;
    return *(int *)((char *)state + offset + 896);
}
