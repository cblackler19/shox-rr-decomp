struct GlobalFlag
{
    unsigned int value;
    unsigned int unused[2];
};

extern "C" GlobalFlag D_0032A894;

extern "C" void func_0012FF10(float* destination, const float* source)
{
    if (!D_0032A894.value) {
        float value = *source;
        ((unsigned int*)destination)[3] = 1;
        destination[2] = value;
    }
}
