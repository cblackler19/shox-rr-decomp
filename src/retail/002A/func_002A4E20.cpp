extern "C" void func_002A4D28(void);

extern "C" void func_002A4E20(void *object) {
    *(void (**)(void))object = func_002A4D28;
    *(int *)((char *)object + 4) = 0;
}
