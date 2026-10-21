extern "C" float func_001112A8(void *object) {
    float value = *(float *)((char *)object + 4);
    void *target = *(void **)((char *)object + 8);
    if (target) {
        void **table = *(void ***)target;
        short adjustment = *(short *)((char *)table + 16);
        float (*method)(void *) = *(float (**)(void *))((char *)table + 20);
        value *= method((char *)target + adjustment);
    }
    return value;
}
