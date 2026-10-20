extern "C" void func_0013BD98(char* destination, const char* source)
{
    if (source != 0) {
        *(int*)(destination + 8) = *(const int*)(source + 0x38);
        *(float*)(destination + 0xC) = *(const float*)(source + 0x28);
    }
}