extern "C" void func_0027E698(void *object, int value) {
    int *words = (int *)object;
    int flags = words[5];
    words[2] = value;
    words[5] = flags | 4;
}
