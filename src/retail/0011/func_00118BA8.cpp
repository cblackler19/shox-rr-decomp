struct Record_18BA8 {
    unsigned char unused[56];
    int value;
};
extern "C" int D_0044AC30 __attribute__((section(".data")));
extern "C" void func_00103198(Record_18BA8 *);
extern "C" void func_00118BA8(Record_18BA8 *record)
{
    record->value = (int)&D_0044AC30;
    func_00103198(record);
}
