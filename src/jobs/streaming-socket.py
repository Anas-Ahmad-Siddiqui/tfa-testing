# import json
# import socket
# import time
# import pandas as pd

# def handle_date(obj):
#     if isinstance(obj, pd.Timestamp):
#         return obj.strftime('%Y-%m-%d %H:%M:%S')
#     raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

# def send_data_over_socket(file_path, host='127.0.0.1', port=9999, chunk_size=2):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     s.listen(1)
#     print(f"Listening for connections on {host}:{port}")

#     last_sent_index = 0
#     while True:
#         conn, addr = s.accept()
#         print(f"Connection from {addr}")
#         try:
#             with open(file_path, 'r') as file:
#                 # skip the lines that were already sent
#                 for _ in range(last_sent_index):
#                     next(file)

#                 records = []
#                 for line in file:
#                     records.append(json.loads(line))
#                     if(len(records)) == chunk_size:
#                         chunk = pd.DataFrame(records)
#                         print(chunk)
#                         for record in chunk.to_dict(orient='records'):
#                             serialize_data = json.dumps(record, default=handle_date).encode('utf-8')
#                             conn.send(serialize_data + b'\n')
#                             time.sleep(5)
#                             last_sent_index += 1

#                         records = []
#         except (BrokenPipeError, ConnectionResetError):
#             print("Client disconnected.")
#         finally:
#             conn.close()
#             print("Connection closed")

# if __name__ == "__main__":
#     send_data_over_socket("datasets/example_2.json")

############################################################################################################


import socket
import csv
import json
import time

def send_data_over_socket(file_path, host='127.0.0.1', port=9999, chunk_size=4):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Listening for connections on {host}:{port}")

    last_sent_index = 0
    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr}")

        try:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for row in csv_reader:
                    print(row)
                    print("\n")
                    json_data = {"date": row[0], "time": row[1], "security": row[2], "verb": row[3], "price": row[4], "qty": row[5], "client": row[6]}
                    record_json = json.dumps(json_data).encode('utf-8')
                    conn.send(record_json + b'\n')
                    time.sleep(5)
                    last_sent_index += 1

        except (BrokenPipeError, ConnectionResetError):
            print("Client disconnected.")
        finally:
            conn.close()
            print("Connection closed")

# Call the function to send data over the socket
send_data_over_socket("datasets/sample-trades.csv")
