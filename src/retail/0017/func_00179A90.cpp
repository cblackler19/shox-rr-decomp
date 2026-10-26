typedef int Quad_179A90 __attribute__((mode(TI)));
struct QuadBlock_179A90 { Quad_179A90 values[4]; };
struct Record_179A90 {
    unsigned char unused[256];
    QuadBlock_179A90 block;
};
extern "C" void func_00179A90(Record_179A90 *destination, const QuadBlock_179A90 *source)
{
    destination->block.values[0] = source->values[0];
    QuadBlock_179A90 *block = (QuadBlock_179A90 *)((char *)destination + 256);
    block->values[1] = source->values[1];
    block->values[2] = source->values[2];
    block->values[3] = source->values[3];
}
