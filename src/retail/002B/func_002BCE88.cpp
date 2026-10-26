extern "C" int func_002BCE88(void *, void *object) {
    char *bytes = (char *)object;
    *(unsigned long long *)(bytes + 72) = 0;
    *(int *)(bytes + 4) = 0x2000;
    return 0;
}
