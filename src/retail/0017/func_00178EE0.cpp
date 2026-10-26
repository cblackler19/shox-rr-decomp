struct Handler_178EE0 { unsigned char unused[64]; short offset; short padding; void (*callback)(void *); };
struct Record_178EE0 { Handler_178EE0 *handler; };
extern "C" void func_00178EE0(Record_178EE0 *record)
{
    Handler_178EE0 *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
