extern "C" char D_00446788[];
extern "C" void func_002C9170(void *resource);
extern "C" void func_001A6050(void *object);

extern "C" void func_00103198(void *object, unsigned flags) {
    *(char **)((char *)object + 0x38) = D_00446788;
    if (*(int *)((char *)object + 0x24) != 0) {
        *(int *)((char *)object + 0x24) = 0;
        func_002C9170(*(void **)((char *)object + 0x1C));
    }
    if (flags & 1)
        func_001A6050(object);
}