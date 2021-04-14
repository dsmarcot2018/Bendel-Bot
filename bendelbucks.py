import constants
from datetime import datetime, timedelta


class BendelBucks:
    """Manage all functionality around Bendel Bucks."""

    def __init__(self):
        self.file = "bbdata.txt"
        self.user_list = ""
        self.remaining_time = 0

    def create_user(self, user_id):
        with open(self.file, 'r') as f:
            line_id = f.readline()
            while line_id:
                split_line = line_id.split(',')
                stored_id = split_line[0]
                if str(stored_id) == str(user_id):
                    print("User already exists.")
                    return
                line_id = f.readline()

        with open(self.file, 'a') as f:
            # User ID, Balance, Hourly, Daily, Weekly, endline
            f.write(f'{user_id},0,None,None,None,\n')

    def add_balance(self, user_id, to_add, *timeout):
        return_string = ""
        with open(self.file, 'r+') as f:
            # Line containing the user id
            found_line = False
            # Has the allowed time passed
            do_write = False
            # Index of the line
            line_index = 0
            # Byte count of the start of the line of the current line
            line_byte = f.tell()
            # Line containing data of the user
            line_data = f.readline()
            while line_data:
                # List [User ID, Balance, Hourly, Daily, Weekly]
                split_line = line_data.split(',')
                stored_id = split_line[0]
                print(f"stored_id: {stored_id}")
                print(f"user_id: {user_id}")

                if str(stored_id) == str(user_id):
                    self.user_list = split_line
                    found_line = True
                    break
                # Getting line of user data from text file
                line_data = f.readline()
                # Increment line index
                line_index += 1
                # Remembering to position where cursor would be
                line_byte = f.tell()
            if not found_line:
                self.create_user(user_id)
                return_string = "New User added, try command again."
                return return_string
            # Adding balance
            stored_balance = int(self.user_list[1])
            stored_balance += to_add
            self.user_list[1] = str(stored_balance)

            # Converting tuple into a string
            for n in timeout:
                timeout = n
            # Checking if optional argument exists
            if timeout:
                if timeout == constants.HOURLY_TIMEOUT:
                    do_write = self.verify_time(self.user_list[2], timeout)
                elif timeout == constants.DAILY_TIMEOUT:
                    do_write = self.verify_time(self.user_list[3], timeout)
                elif timeout == constants.WEEKLY_TIMEOUT:
                    do_write = self.verify_time(self.user_list[4], timeout)
                if do_write:
                    if timeout == constants.HOURLY_TIMEOUT:
                        self.user_list[2] = datetime.now()
                    elif timeout == constants.DAILY_TIMEOUT:
                        self.user_list[3] = datetime.now()
                    elif timeout == constants.WEEKLY_TIMEOUT:
                        self.user_list[4] = datetime.now()
            else:
                do_write = True

            # Writing to file
            # The else only ever triggers due to not enough time between calls
            if do_write:
                line = ""
                # Format line
                for i in self.user_list:
                    line += f"{i},"
                line = line[:-1]
                # Reset cursor position in file
                f.seek(0)
                # List of all lines in file
                contents = f.readlines()
                # Replacing line where it matches with user_id
                contents[line_index] = line
                # Converting list into string for writing
                contents = "".join(contents)
                # Reset cursor position in file
                f.seek(0)
                # Writing to file
                f.write(contents)
                # Message sent to discord
                return_string = f"Added ${to_add}."
            else:
                # Message sent to discord
                return_string = f"You must wait " \
                                f"{round(self.remaining_time)}s to claim."
            return return_string

    def verify_time(self, last_called, time_out):
        now_time = datetime.now()

        if last_called == "None":
            print("None reached")
            return True
        last_called = datetime.fromisoformat(last_called)
        time_difference = now_time - last_called
        seconds_passed = time_difference.total_seconds()
        if seconds_passed > time_out:
            print("Comparison Reached")
            return True
        else:
            print("Else Reached")
            self.remaining_time = time_out - seconds_passed
            return False


# with open("bbdata.txt", "r") as f:
#     contents = f.readlines()
#     print("Reading")
#     print(contents)
#     append = "164512645427232769,105,2021-04-14 01:39:34.370039,2021-04-14 01:39:15.478595,None,end"
#     contents.append(append)
#
# with open("bbdata.txt", "w") as f:
#     contents = "\n".join(contents)
#     print("Writing")
#     print(contents)
#     f.write(contents)