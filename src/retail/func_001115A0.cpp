struct State_49B808 { void *first; void *second; unsigned int reserved[2]; };
extern "C" State_49B808 D_49B808;
extern "C" void func_001115D0(State_49B808 *);
extern "C" void func_001115A0(void *first, void *second) {
    D_49B808.first = second;
    D_49B808.second = first;
    func_001115D0(&D_49B808);
}
