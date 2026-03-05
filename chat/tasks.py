# chat/tasks.py (Conceptual)
def cleanup_delivered_messages():
    Message.objects.filter(is_delivered=True).update(text="[Encrypted/Delivered]", is_archived_locally=True)