import constants
from datetime import datetime, timedelta

class BendelBucks:
    """Manage all functionality around Bendel Bucks."""

    def __init__(self):
        self.file = "bbdata.txt"
        self.user_list = ""

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
            # User ID, Balance, Hourly, Daily, Weekly, endline
            f.write(f'{user_id},0,None,None,None,end\n')

    def add_balance(self, user_id, to_add, *method):
        return_string = ""
        with open(self.file, 'r+') as f:
            # Line containing the user id
            found_line = False
            # Has the allowed time passed
            do_write = False
            # Byte count of the start of the line of the current line
            line_byte = f.tell()
            # Line containing data of the user
            line_data = f.readline()
            while line_data:
                # List [User ID, Balance, Hourly, Daily, Weekly, endline]
                split_line = line_data.split(',')
                stored_id = split_line[0]
                if str(stored_id) == str(user_id):
                    self.user_list = split_line
                    found_line = True
                    break
                line_data = f.readline()
                line_byte = f.tell()
                if not found_line:
                    return
            stored_balance = int(self.user_list[1])
            stored_balance += to_add
            self.user_list[1] = str(stored_balance)

            do_write = True

            # if method == "Hourly":
            #     current_time = datetime.now()
            #     if split_line[2] == "None":
            #         current_bal = int(split_line[1])
            #         current_bal += constants.DAILY_REWARD
            #         split_line[1] = str(current_bal)
            #         split_line[2] = str(current_time)
            #         return_string = f"added {constants.DAILY_REWARD}"
            #         do_write = True
            #     else:
            #         last_called = datetime.fromisoformat(split_line[2])
            #         time_difference = current_time - last_called
            #         if time_difference > constants.HOURLY_TIMEOUT:
            #             current_bal = int(split_line[1])
            #             current_bal += constants.DAILY_REWARD
            #             split_line[1] = str(current_bal)
            #             split_line[2] = str(current_time)
            #             return_string = f"added {constants.DAILY_REWARD}"
            #             do_write = True
            #         else:
            #             remaining_time = constants.HOURLY_TIMEOUT -\
            #                              time_difference
            #             return_string = f"must wait \
            #             {round(remaining_time)}s"

            if do_write:
                line = ""
                for i in self.user_list:
                    line += f"{i},"
                line = line[:-1]
                f.seek(line_byte)
                f.write(line)
            return return_string

    def edit_time_log(self, file_bytes, time_command):
        return


with open("bbdata.txt", 'r+') as f:
    print(f.readline())
    f.write("hello")

bb = BendelBucks()

bb.add_balance(819039754611326976, 100)

with open("bbdata.txt", 'r+') as f:
    print(f.readline())
