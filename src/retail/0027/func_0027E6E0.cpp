extern "C" void func_0027E6E0(void *object, float value) {
    int *words = (int *)object;
    int flags = words[5];
    *(float *)((char *)object + 32) = value;
    words[5] = flags | 2;
}
