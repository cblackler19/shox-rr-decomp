struct Record {
    int value;
    const void *type;
    int data;
};

extern "C" char D_004675E8[];

extern "C" void func_002671C0(Record *record, int value, int data)
{
    if (record == 0)
        return;
    record->data = data;
    record->value = value;
    record->type = D_004675E8;
}
