extern "C" float func_00123370(void *base, int index) {
    char *records = (char *)base + 0x1ECCC;
    char *record = records + index * 16;
    return *(float *)record;
}
