struct Source {
    unsigned int index;
    unsigned int value;
};

extern "C" void func_00158E20(unsigned int* target, const Source* source) {
    target += source->index;
    target[2] = source->value;
}
