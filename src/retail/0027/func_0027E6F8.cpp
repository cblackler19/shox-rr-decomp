extern "C" void func_0027E6F8(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[11] = value;
    words[5] = flags | 0x400;
}
