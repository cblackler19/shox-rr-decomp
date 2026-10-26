struct Handler_14FBF0 { unsigned char unused[24]; short offset; short padding; void (*callback)(void *); };
struct Record_14FBF0 { Handler_14FBF0 *handler; };
extern "C" void func_0014FBF0(Record_14FBF0 *record)
{
    Handler_14FBF0 *handler = record->handler;
    handler->callback((char *)record + handler->offset);
}
