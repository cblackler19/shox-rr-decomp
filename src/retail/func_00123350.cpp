extern "C" int func_00123350(void *base, int index) {
    char *records = (char *)base + 0x1ECD4;
    char *record = records + index * 16;
    return *(int *)record;
}
