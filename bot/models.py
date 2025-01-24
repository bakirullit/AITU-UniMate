profiles = []

# Класс для связанного списка (лайки)
class LikeNode:
    def __init__(self, user_id):
        self.user_id = user_id
        self.next = None

class LikeList:
    def __init__(self):
        self.head = None

    def add_like(self, user_id):
        new_node = LikeNode(user_id)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_likes(self):
        current = self.head
        likes = []
        while current:
            likes.append(current.user_id)
            current = current.next
        return likes

like_list = LikeList()