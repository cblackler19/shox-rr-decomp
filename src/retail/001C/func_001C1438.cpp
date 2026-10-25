typedef unsigned int uint128 __attribute__((mode(TI)));
extern "C" void func_001C1438(void *destination, const void *source) {
    *(uint128 *)((char *)destination + 336) = *(const uint128 *)source;
}
