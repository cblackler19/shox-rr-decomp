struct Record {
    unsigned int pad[6];
    unsigned int mask;
    unsigned int count;
    unsigned int flags;
};

extern "C" Record *func_00276298(Record *record, unsigned int shift)
{
    record->count = 0;
    record->flags = 0;
    record->mask = (1u << shift) - 1;
    return record;
}
