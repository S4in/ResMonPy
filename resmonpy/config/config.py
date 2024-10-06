import os


class Config:
    def __init__(self, directory="C:\\Temp\\resmonpy", data_format="csv"):
        self.directory = directory
        self.data_format = data_format
        self.verify_dir()

    def verify_dir(self):

        temp_dir = os.path.dirname(self.directory)

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

