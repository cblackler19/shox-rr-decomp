extern "C" void func_00160100(int* base, const int* index)
{
    int* selected = base + index[0];
    selected[2] = 1;
}