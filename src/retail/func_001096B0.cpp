extern "C" int func_001096B0(void *object, void **result) {
    if (*(void **)((char *)object + 0x1F4)) {
        *result = (char *)object + 0x1A0;
        return *(void **)((char *)object + 0x1F4) != 0;
    }
    return 0;
}
