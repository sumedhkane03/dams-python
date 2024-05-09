import socket
import struct

def create_client(host='10.200.61.12', port=6672):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the client to the server
    server_address = (host, port)
    print(f"Connecting to {host} on port {port}...")
    client_socket.connect(server_address)

    try:
        # Send some data to the server
        message = "Hello, Server!"
        print(f"Sending: {message}")
        client_socket.sendall(message.encode())

        # Prepare to receive data
        # This buffer size can be adjusted depending on the expected data size
        buffer_size = 57344  # 1 KB size buffer, adjust based on your needs
        full_data = []


        while True:
            # Receive data from the server
            data = client_socket.recv(buffer_size)
            #first two bytes: 16bit unsigned int, next four bytes: 32bit unsigned int, next 1 byte: 8bit unsigned int
            if not data:
                print("no data received :(")
                break  # If no data is received, break out of the loop
            first_two_bytes = struct.unpack('<H', data[:2])[0]
            next_four_bytes = struct.unpack('<I', data[2:6])[0]
            next_byte = struct.unpack('<B', data[6:7])[0]

            first_two_bytes = (first_two_bytes * (90/16384))
            next_four_bytes = (next_four_bytes / 4)
            
            #shift next_bite to the left by 2
            next_byte = (next_byte >> 2)

            full_data.append([first_two_bytes, next_four_bytes, next_byte])
            print([first_two_bytes, next_four_bytes, next_byte])
            print(full_data)
            #save full_data to a file called data.txt
            with open('data.txt', 'w') as f:
                f.write(str(full_data))
            


            #break
        
    finally:
        # Close the socket to clean up
        client_socket.close()
        print("Connection closed.")
        print(full_data)

if __name__ == "__main__":
    create_client()
