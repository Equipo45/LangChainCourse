import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

encoded_string = encoding.encode("sdfnkljsdfjklsd")

print("*Frase tokenizada*")
print(encoded_string)

decoded_string = encoding.decode(encoded_string)

print("*Frase destokenizada*")
print(decoded_string)
