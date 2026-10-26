extern "C" void func_00178C28(float *object, float value) {
    float *fields = (float *)((char *)object + 28);
    fields[2] += value * fields[5];
}
