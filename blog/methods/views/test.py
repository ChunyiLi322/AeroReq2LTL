import re
text = "The system will transfer to the System Initialization state if a reset exception is received..\nIn the Fault Recovery state the system is reconfigured..\nIf a single permanent fault has occurred, for example, the system will, when the transfer is made back to Normal Operation state, be capable of handling another fault."
text_len = re.findall(r'\n', text)
len_value = len(text_len) + 1
print("------------text_len---------------", text_len)
print("------------text_len----type-----------", type(text_len))
print("------------需要转化几个公式---------------", len_value)

