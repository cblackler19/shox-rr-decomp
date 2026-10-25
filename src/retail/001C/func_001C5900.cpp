struct Chunk_001C5900 {
    int values[2048];
    int tail[2];
};

extern "C" void func_001C5900(void *self) {
    Chunk_001C5900 *base = (Chunk_001C5900 *)self;
    base->values[2048] = 0;
    base->tail[1] = 0;
    Chunk_001C5900 *shifted = (Chunk_001C5900 *)((char *)self + 8208);
    shifted->values[2048] = 0;
    shifted->tail[1] = 0;
}
