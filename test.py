def print_title(s, char, len_title):
    len_char = len_title - len(s) - 2

    if len_char < 2:
        return s
    elif len_char % 2 == 0:
        head = tail = char * (len_char // 2)
    else:
        head = char * (len_char // 2)
        tail = head + char

    return head + " " + s + " " + tail


s = "hello world"
title = print_title(s, "=", 120)

print(title)
print(len(s))
print(len(title))
