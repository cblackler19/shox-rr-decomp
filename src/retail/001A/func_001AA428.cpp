struct ShortCell { short value; unsigned int unused[2]; };
struct WordCell { unsigned int value; unsigned int unused[2]; };
extern "C" ShortCell D_0052BBBC;
extern "C" ShortCell D_0052BBBE;
extern "C" WordCell D_0052BBC0;
extern "C" WordCell D_0052BBC4;

extern "C" void func_001AA428(short first, int second, int third)
{
    ShortCell* firstCell = &D_0052BBBC;
    ShortCell* zeroCell = &D_0052BBBE;
    WordCell* secondCell = &D_0052BBC0;
    WordCell* thirdCell = &D_0052BBC4;
    firstCell->value = first;
    secondCell->value = second;
    thirdCell->value = third;
    zeroCell->value = 0;
}
