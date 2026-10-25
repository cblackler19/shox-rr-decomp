extern "C" void func_001110D0(void *object, float value) {
    if (value < 0.0f)
        value = 0.0f;
    if (value > 1.0f)
        value = 1.0f;
    *(float *)((char *)object + 4) = value;
}
