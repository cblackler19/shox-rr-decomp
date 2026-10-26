extern "C" void func_001A3AE8(void *object) {
    char *bytes = (char *)object;
    bytes[0x204] = 0;
    *(int *)(bytes + 0x208) = 0;
    *(int *)(bytes + 0x20C) = 0;
    bytes[4] = 0;
}
