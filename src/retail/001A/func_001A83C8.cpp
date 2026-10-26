struct Pair_1A83C8 { int first; int second; };
extern "C" void func_001A6678(int, int);
extern "C" void func_001A83C8(void *, Pair_1A83C8 *pair)
{
    if (pair)
        func_001A6678(pair->first, pair->second);
}
