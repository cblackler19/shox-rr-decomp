extern "C" void func_0028E2A8(void *object, int value) {
    int *words = (int *)object;
    words[0x1BBC / 4] = 0;
    words[0x1BB0 / 4] = value;
    words[0x1BB8 / 4] = 0;
    words[0x1BB4 / 4] = value;
}
