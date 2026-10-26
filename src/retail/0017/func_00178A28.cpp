typedef int Quad_178A28 __attribute__((mode(TI)));
struct QuadBlock_178A28 { Quad_178A28 values[4]; };
struct Record_178A28 {
    unsigned char unused[160];
    QuadBlock_178A28 block;
};
extern "C" void func_00178A28(Record_178A28 *destination, const QuadBlock_178A28 *source)
{
    destination->block.values[0] = source->values[0];
    QuadBlock_178A28 *block = (QuadBlock_178A28 *)((char *)destination + 160);
    block->values[1] = source->values[1];
    block->values[2] = source->values[2];
    block->values[3] = source->values[3];
}
