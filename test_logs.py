from logger import setup_logger


test_logger = setup_logger("test_logger", "test.log")

class User(object):
    def __init__(self, name, passwd) -> None:
        self.name = name
        self.passwd = passwd
        
        
def create_user_info():
    user = User("name", "passwd")
    return user

def create_user_warn():
    user = User("name")
    return user
        

for _ in range(10):
    try:
        create_user_info()
        test_logger.info("User created successfully")
        create_user_warn()
    except Exception as e:
        test_logger.warning(f"Unable to create a user. Erorr: {e}")



