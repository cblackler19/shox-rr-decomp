extern "C" char D_0035BF5C[];

extern "C" void func_00261C60(void *object, int value) {
    if (D_0035BF5C[0] == 0)
        value = 0;
    *(int *)((char *)object + 8) = value;
}
