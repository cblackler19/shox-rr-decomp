extern "C" float func_00123390(void *base, int index) {
    char *records = (char *)base + 0x1ECC8;
    char *record = records + index * 16;
    return *(float *)record;
}
