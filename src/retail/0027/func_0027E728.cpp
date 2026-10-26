extern "C" void func_0027E728(void *object, float value) {
    int *words = (int *)object;
    int flags = words[5];
    *(float *)((char *)object + 0xAC) = value;
    words[5] = flags | 0x10;
}
