import json

class UserInteraction:
    
    FILE_PATH = "users.json"
    
    @classmethod
    def add_user(cls, user_id):
        try:
            with open(cls.FILE_PATH, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        if user_id in data:
            return "уже привязан к уведомлениям"
        data.append(user_id)
        
        with open(cls.FILE_PATH, 'w') as file:
            json.dump(data, file)
            return "успешно привязан к уведомлениям"
            
    @classmethod
    def get_alert(cls, announcement="ТРЕВОГА"):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        mentions = [f"[ping](tg://user?id={uid})" for uid in data]
        message = ", ".join(mentions)
        
        return f"{message}\n{announcement}"
    
    @classmethod
    def remove_user(cls, user_id):
        try:
            with open(cls.FILE_PATH, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            
        if user_id in data:
            data.remove(user_id)
            
            with open(cls.FILE_PATH, 'w') as file:
                json.dump(data, file)
            return "Успех!"
        
        else:
            return "Вы не были подписаны на уведомления"
        