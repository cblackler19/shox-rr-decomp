typedef unsigned int uint128 __attribute__((mode(TI)));
extern "C" void func_001C1458(void *destination, const void *source) {
    *(uint128 *)((char *)destination + 368) = *(const uint128 *)source;
}
