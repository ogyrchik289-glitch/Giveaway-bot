import random
import asyncio

class Gieveaway:
    def __init__(self, chat_id: int, message_id: int, text: str):
        self.participants: set[int] = set()
        self.chat_id = chat_id
        self.message_id = message_id
        self.is_active = True
        self.text = text
        self.task: asyncio.Task | None = None
        
    def add_participant(self, user_id: int) -> bool:
        if user_id not in self.participants:
            self.participants.add(user_id)
            return True
        else:
            return False
        
    def draw_winner(self) -> list:
        self.is_active = False
        if len(self.participants) >= 3:
            first = random.choice(list(self.participants))
            self.participants.remove(first)
            second = random.choice(list(self.participants))
            self.participants.remove(second)
            third = random.choice(list(self.participants))
            return [first, second, third]
        elif len(self.participants) == 2:
            first = random.choice(list(self.participants))
            self.participants.remove(first)
            second = random.choice(list(self.participants))
            return [first, second]
        else:
            return [random.choice(list(self.participants))]    
        
        
        