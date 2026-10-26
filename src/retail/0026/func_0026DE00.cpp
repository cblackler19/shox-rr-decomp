extern "C" void func_0026DE00(void *object, int value) {
    int *words = (int *)object;
    int flags = words[3];
    words[4] = value;
    words[3] = flags | 0x40;
}
