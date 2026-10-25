extern "C" int func_00109238(void *object, void **result) {
    if (*(void **)((char *)object + 0x6C)) {
        *result = (char *)object + 0x5C;
        return *(void **)((char *)object + 0x6C) != 0;
    }
    return 0;
}
