extern "C" void func_0027E758(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[1] = value;
    words[5] = flags | 8;
}
