struct func_0010A668_Node { int pad0; void *next; };
struct func_0010A668_Callback { unsigned char pad0[0x30]; short offset; short pad34; void (*call)(void *); };
struct func_0010A668_State { int pad0; void *pad4; void *node; void *owner; int pad10; func_0010A668_Callback *callback; };

extern "C" void func_0010A668(func_0010A668_Node *node, func_0010A668_State *state) {
    void *next = node->next;
    state->owner = node;
    state->node = next;
    node->next = state;
    state->callback->call((char *)state + state->callback->offset);
}
