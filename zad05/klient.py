import sysv_ipc
import os
import time

input_queue_key = 1234
output_queue_key = 5678

input_queue = sysv_ipc.MessageQueue(input_queue_key)
output_queue = sysv_ipc.MessageQueue(output_queue_key)

client_pid = os.getpid()
print(f"PID: {client_pid}")

words_to_translate = ["jabłko", "kot", "pies"]
print(f"Słowa do przetłumaczenia: {words_to_translate}")

for word in words_to_translate:
    input_queue.send(word.encode(), type=client_pid)

responses_received = 0
while responses_received < len(words_to_translate):
    if output_queue.current_messages > 0:
        response, message_type = output_queue.receive()

        if message_type != client_pid:
            continue

        translated_word = response.decode()
        print(f"Tłumaczenie: {translated_word}")
        responses_received += 1
    else:
        time.sleep(0.1)

print("Wszystko przetłumaczone, zamknięcie klienta")