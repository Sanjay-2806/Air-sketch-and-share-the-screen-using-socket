
import socket
import cv2 as cv
import numpy as np
import struct

PORT = 9999
server = socket.socket()
server.bind(('0.0.0.0', PORT))
server.listen(1)
print(f"waiting for sender on port {PORT}...")

conn, addr = server.accept()
print(f"coonnected to: {addr}")

while True:
    try:
        packedsize = conn.recv(4)
        if not packedsize:
            break
        size = struct.unpack('>L', packedsize)[0]

        
        data = b''
        while len(data) < size:
            packet = conn.recv(size - len(data))
            if not packet:
                break
            data += packet

        imgarray = np.frombuffer(data, dtype=np.uint8)
        img = cv.imdecode(imgarray, cv.IMREAD_COLOR)
        if img is not None:
            cv.imshow("receiver - remote drawing", img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("Errrror occuredd :", e)
        break

conn.close()
cv.destroyAllWindows()



