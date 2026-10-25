extern "C" int func_001291A0(int** object)
{
    int* child = *object;
    if (child == 0 || child[2] == 0) {
        return 0;
    }
    return child[3];
}