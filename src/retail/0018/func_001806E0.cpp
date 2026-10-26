struct Record_1806E0 { int value; };
extern "C" int D_00455190 __attribute__((section(".data")));
extern "C" void func_00177380(Record_1806E0 *);
extern "C" void func_001806E0(Record_1806E0 *record)
{
    record->value = (int)&D_00455190;
    func_00177380(record);
}
