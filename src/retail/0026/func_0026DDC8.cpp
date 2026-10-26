extern "C" void func_0026DDC8(void *object, int value) {
    int *words = (int *)object;
    int flags = words[3];
    words[6] = value;
    words[3] = flags | 0x4000;
}
