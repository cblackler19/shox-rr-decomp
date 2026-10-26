struct Record_17A0A8 { int value; };
extern "C" int D_00454F50 __attribute__((section(".data")));
extern "C" void func_001806E0(Record_17A0A8 *);
extern "C" void func_0017A0A8(Record_17A0A8 *record)
{
    record->value = (int)&D_00454F50;
    func_001806E0(record);
}
