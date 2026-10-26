extern "C" void func_0026DC48(void *object, int value) {
    int *words = (int *)object;
    int flags = words[3];
    words[5] = value;
    words[3] = flags | 2;
}
