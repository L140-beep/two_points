import matplotlib.pyplot as plt
import socket
import numpy as np
from skimage.measure import label
from skimage.measure import regionprops
     
host = "84.237.21.36"
port = 5152

packet_size = 40002

def recvall(sock, n):
    data = bytearray()
    
    while len(data) < n:
        packet = sock.recv(n - len(data))
        
        if not packet:
            return -1

        data.extend(packet)
        
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suck:
    suck.connect((host, port))
    count = 0
    
    while(count != 10):
        suck.send(b"get")
        bts = recvall(suck, packet_size)    
        rows, cols = bts[:2]  
        
        image = np.frombuffer(bts[2:rows * cols + 2], 
                            dtype='uint8').reshape(rows, cols)
        
        t_image = image.copy()
        t_image[t_image > 0] = 1
        t_image = label(t_image)
        regions = regionprops(t_image)
        
        dots_count = t_image.max()
        
        if dots_count < 2:
            continue
        
        pos1 = regions[0]["centroid"]
        pos2 = regions[1]["centroid"]

        result = np.round(np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2), 1)
        print(result)
        suck.send(f"{result}".encode())
        validation = suck.recv(20)
        print(validation)
        
        if(validation == b"yep"):
            count += 1
        
            


print("Done!")

