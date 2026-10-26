extern "C" void func_0026DE18(void *object, int value) {
    int *words = (int *)object;
    int flags = words[3];
    words[2] = value;
    words[3] = flags | 0x80;
}
