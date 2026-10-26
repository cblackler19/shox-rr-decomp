extern "C" void *func_001A4830(void *, void **slot) {
    char *pointer = (char *)*slot;
    void *value = *(void **)pointer;
    *slot = value;
    return pointer + 8;
}
