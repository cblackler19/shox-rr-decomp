extern "C" void func_0027E680(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[24] = value;
    words[5] = flags | 0x1000;
}
