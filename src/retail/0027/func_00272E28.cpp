extern "C" unsigned int func_00272E28(unsigned int *object, unsigned int value) {
    object[11] = value;
    if (value >= 65)
        object[11] = 64;
    return object[11];
}
