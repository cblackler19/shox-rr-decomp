extern "C" void func_001600C0(int *entries, const int *index) {
    if (index) {
        int *entry = entries + *index;
        entry[2] = 1;
    }
}
