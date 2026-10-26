struct Tail_153DF8 {
    unsigned char unused[8];
    int field8;
    int field12;
    int field16;
    int field20;
    int field24;
    int field28;
    int field32;
    int field36;
};
extern "C" void func_00153DF8(void *record)
{
    Tail_153DF8 *tail = (Tail_153DF8 *)((char *)record + 44);
    tail->field32 = 0;
    tail->field16 = 0;
    tail->field12 = 0;
    tail->field24 = 0;
    tail->field20 = 0;
    tail->field28 = 0;
    tail->field8 = 0;
    tail->field36 = 0;
}
