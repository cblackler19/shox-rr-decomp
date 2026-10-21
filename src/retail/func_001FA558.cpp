struct Record {
    int first;
    int second;
    int third;
};

extern "C" void func_001FA558(Record *record, int value) {
    record->third = value + 0x14;
    record->second = 0x100;
    record->first = 0;
}
