from config_reader import ConfigReader


config_reader = ConfigReader()
app_config = config_reader.read_config("./config.yaml")
print("This is some app.")
print("Configuration parameters are: ")
for par in app_config:
    print(par,":", end=" ")
    print(app_config[par])

