extern "C" void func_001A6050(void *resource);

struct ResourceNode
{
    ResourceNode *next;
    ResourceNode *previous;
    void *resource0;
    void *resource1;
    void *resource2;
};

struct ResourceList
{
    ResourceNode *head;
    ResourceNode *tail;
    int count;
};

extern "C" void func_001024E0(ResourceList *list)
{
    ResourceNode *cursor = list->head;
    if (cursor != 0) {
        ResourceNode *next;
        void **resources;
        do {
            ResourceNode *node = cursor;
            next = node->next;
            cursor = next;
            if (list->head == node) {
                list->head = next;
                if (next != 0)
                    next->previous = 0;
            } else if (list->tail == node) {
                list->tail = node->previous;
                if (list->tail != 0)
                    list->tail->next = 0;
            } else {
                node->previous->next = node->next;
                node->next->previous = node->previous;
            }

            if (node != 0) {
                resources = &node->resource0;
                if (resources[0] != 0)
                    func_001A6050(resources[0]);
                if (resources[1] != 0)
                    func_001A6050(resources[1]);
                if (resources[2] != 0)
                    func_001A6050(resources[2]);
                func_001A6050(node);
            }
            list->count--;
        } while (next != 0);
    }
}
