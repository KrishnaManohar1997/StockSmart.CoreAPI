chat = open(input("Enter File name : "))

chat_text_content = chat.read()  # read its contents

chat.close()
import re

cleared_text = re.sub(
    "(\d+\/\d+\/\d+)(,)(\s)(\d+:\d+)(\s)(\w+)(\s)(-)(\s\w+)*(:)|<Media omitted>",
    "",
    chat_text_content,
)
print(cleared_text)
