extern "C" void func_0027E710(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[10] = value;
    words[5] = flags | 0x20;
}
