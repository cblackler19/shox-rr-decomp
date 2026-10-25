struct LookupEntry {
    unsigned int key;
    unsigned int value;
};

extern "C" LookupEntry D_597BD0[128];

extern "C" void func_00100F68(unsigned int key) {
    for (unsigned int i = 0; i < 128; ++i) {
        if (D_597BD0[i].key == key) {
            D_597BD0[i].value = 0;
            return;
        }
    }
}
