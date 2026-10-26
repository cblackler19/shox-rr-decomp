struct Node_238F40 { int reserved; int value; };
struct State_238F40 { Node_238F40 *node; };
extern "C" void func_002C0090(int, int, int);
extern "C" void func_00238F40(State_238F40 *state)
{
    func_002C0090(state->node->value, 0, 1);
}
