extern "C" void func_00221FE8(void *object) {
    char *bytes = (char *)object;
    *(int *)bytes = 0;
    *(unsigned short *)(bytes + 32) = 0;
    *(unsigned short *)(bytes + 34) = 0;
    *(unsigned short *)(bytes + 36) = 0;
}
