extern "C" void func_0027E740(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[0] = value;
    words[5] = flags | 0x80;
}
