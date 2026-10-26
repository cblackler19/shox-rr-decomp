extern "C" void func_00178C08(float *object, float value) {
    float *fields = (float *)((char *)object + 4);
    fields[2] += value * fields[5];
}
