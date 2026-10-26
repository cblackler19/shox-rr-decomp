extern "C" void func_0027E6B0(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[22] = value;
    words[5] = flags | 0x800;
}
