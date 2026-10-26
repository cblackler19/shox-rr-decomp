struct Node_00269A58 { int value0; int value1; int value2; int value3; int value4; int value5; };
extern "C" Node_00269A58 *D_0058A790 __attribute__((section(".data")));
extern "C" void func_00269A58(int value, Node_00269A58 *node)
{
    node->value3 = value;
    node->value5 = (int)D_0058A790;
    D_0058A790 = node;
    node->value2 = value;
    node->value0 = 0;
    node->value4 = 0;
    node->value1 = 0;
}
