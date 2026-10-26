struct Record_12AE70 {
    unsigned char unused[16];
    int index;
};
extern "C" void func_0012E288(void *);
extern "C" void func_0012AE70(Record_12AE70 *record)
{
    int offset = record->index * 4 + 12;
    func_0012E288((char *)record + offset);
}
