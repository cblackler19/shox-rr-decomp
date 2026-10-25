struct SourcePair { int flag; int value; };
struct DestinationAt8 { int unused[2]; int value; };
extern "C" void func_00153DA0(DestinationAt8* destination, SourcePair* source) {
    if (source->flag == 1) {
        destination->value = source->value;
    }
}
