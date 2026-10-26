struct Handler {
    unsigned char unused[80];
    short offset;
    short padding;
    void (*callback)(void *);
};
struct Record {
    unsigned char unused[20];
    Handler *handler;
};

extern "C" void func_0010B928(Record *record)
{
    Handler *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
