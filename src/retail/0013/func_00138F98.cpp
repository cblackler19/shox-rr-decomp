struct Handler_138F98 { unsigned char unused[24]; short offset; short padding; void (*callback)(void *); };
struct Record_138F98 { Handler_138F98 *handler; };
extern "C" void func_00138F98(Record_138F98 *record)
{
    Handler_138F98 *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
