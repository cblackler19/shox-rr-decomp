extern "C" void func_00119818(void* unused, int value, void* object)
{
    int* words = (int*)object;
    int increment = value * words[9] * words[8];
    words[11] += increment;
}
