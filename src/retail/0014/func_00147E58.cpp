struct Handler_147E58 { unsigned char unused[24]; short offset; short padding; void (*callback)(void *); };
struct Record_147E58 { Handler_147E58 *handler; };
extern "C" void func_00147E58(Record_147E58 *record)
{
    Handler_147E58 *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
