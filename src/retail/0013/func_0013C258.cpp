struct Handler_13C258 { unsigned char unused[24]; short offset; short padding; void (*callback)(void *); };
struct Record_13C258 { Handler_13C258 *handler; };
extern "C" void func_0013C258(Record_13C258 *record)
{
    Handler_13C258 *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
