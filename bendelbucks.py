import constants
from datetime import datetime, timedelta

class BendelBucks:
    """Manage all functionality around Bendel Bucks."""

    def __init__(self):
        self.file = "bbdata.txt"

    def create_user(self, user_id):
        with open(self.file, 'r') as f:
            line_id = f.readline()
            while line_id:
                split_line = line_id.split(',')
                stored_id = split_line[0]
                if str(stored_id) == str(user_id):
                    return
                line_id = f.readline()

        with open(self.file, 'a') as f:
            f.write(f'{user_id},0,None,None,None,end\n')

    def add_balance(self, user_id, to_add, method):
        return_string = ""
        with open(self.file, 'r+') as f:
            found_line = False
            do_write = False
            line_byte = f.tell()
            line_id = f.readline()
            while not line_id:
                split_line = line_id.split('\n', 1)
                stored_id = split_line[0]
                if str(stored_id) == str(user_id):
                    found_line = True
                    break
                line_id = f.readline()
                line_byte = f.tell()
            if not found_line:
                return
            if method == "Hourly":
                current_time = datetime.now()
                if split_line[2] == "None":
                    current_bal = int(split_line[1])
                    current_bal += constants.DAILY_REWARD
                    split_line[1] = str(current_bal)
                    split_line[2] = str(current_time)
                    return_string = f"added {constants.DAILY_REWARD}"
                    do_write = True
                else:
                    last_called = datetime.fromisoformat(split_line[2])
                    time_difference = current_time - last_called
                    if time_difference > constants.HOURLY_TIMEOUT:
                        current_bal = int(split_line[1])
                        current_bal += constants.DAILY_REWARD
                        split_line[1] = str(current_bal)
                        split_line[2] = str(current_time)
                        return_string = f"added {constants.DAILY_REWARD}"
                        do_write = True
                    else:
                        remaining_time = constants.HOURLY_TIMEOUT -\
                                         time_difference
                        return_string = f"must wait \
                        {round(remaining_time)}s"
            if do_write:
                line = ""
                for i in split_line:
                    line += f"{i},"
                line = line[:-1]
                f.seek(line_byte)
                f.write()
            return return_string

# with open("bbdata.txt", 'r+') as f:
#     print(f.readline())
#     print(f.tell())
#     f.seek(41)
#     f.write("hello")
