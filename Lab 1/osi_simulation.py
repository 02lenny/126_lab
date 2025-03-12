import json
import struct
import pickle

# Physical Layer
class PhysicalLayer:
    def send(self, data):
        print("[Physical] Encoding to hex the data\t", data)
        encoded = data.hex()
        return encoded.encode()

    def receive(self, data):
        print("[Physical] Decoding from hex the data\t", data)
        decoded = bytes.fromhex(data.decode())
        return decoded

# Data Link Layer
class DataLinkLayer:
    def send(self, data, mac_address):
        print("[DataLink] Framing MAC addr to data\t", data)
        framed_data = f"MAC_HEADER:{mac_address}|".encode() + data
        return framed_data

    def receive(self, data):
        print("[DataLink] Removing MAC addr from data\t", data)
        header, stripped_data = data.split(b'|', 1)
        return stripped_data

# Network Layer
class NetworkLayer:
    def send(self, data, ip_address):
        print("[Network] Adding IP header to data\t", data)
        packet = f"IP_HEADER:{ip_address}|".encode() + data
        return packet

    def receive(self, data):
        print("[Network] Removing IP header from data\t", data)
        header, stripped_packet = data.split(b'|', 1)
        return stripped_packet

# Transport Layer
class TransportLayer:
    def send(self, data):
        print("[Transport] Segmenting data\t\t", data)
        segment = struct.pack('>I', len(data)) + data
        return segment

    def receive(self, data):
        print(f"[Transport] Reassembling Data\t\t", data)
        length = struct.unpack('>I', data[:4])[0]
        reassembled_data = data[4:]
        return reassembled_data

# Session Layer
class SessionLayer:
    def send(self, data):
        print("[Session] Opening session\t")
        session_data = json.dumps({"session": "open", "data": data.hex()}).encode()
        return session_data

    def receive(self, data):
        print("[Session] Closing session\t")
        session_info = json.loads(data.decode())
        stripped = bytes.fromhex(session_info["data"])
        return stripped

# Presentation Layer
class PresentationLayer:
    def send(self, data):
        print("[Presentation] Encoding data\t\t", data)
        encoded_data = pickle.dumps(data)
        return encoded_data

    def receive(self, data):
        print("[Presentation] Decoding data\t\t", data)
        decoded_data = pickle.loads(data)
        return decoded_data

# Application Layer
class ApplicationLayer:
    def send(self, message):
        print("[Application] Sending Request\t")
        request = f"HTTP_REQUEST:{message}".encode()
        return request

    def receive(self, response):
        print("[Application] Receiving response")
        response = response.replace(b"HTTP_REQUEST:", b"")
        return response.decode()

if __name__ == "__main__":
    message = input("Enter message to send: ").encode()

    app = ApplicationLayer()
    pres = PresentationLayer()
    sess = SessionLayer()
    trans = TransportLayer()
    net = NetworkLayer()
    data_link = DataLinkLayer()
    phys = PhysicalLayer()

    ip_address = "192.168.1.1"
    mac_address = "00:1A:2B:3C:4D:5E"

    print("\n--- SENDING DATA ---\n")
    app_data = app.send(message)
    pres_data = pres.send(app_data)
    sess_data = sess.send(pres_data)
    trans_data = trans.send(sess_data)
    net_data = net.send(trans_data, ip_address)
    data_link_data = data_link.send(net_data, mac_address)
    phys_data = phys.send(data_link_data)

    print("\nSent Data:", phys_data)

    print("\n\n--- RECEIVING DATA ---\n")
    data_received = phys.receive(phys_data)
    data_received = data_link.receive(data_received)
    data_received = net.receive(data_received)
    data_received = trans.receive(data_received)
    data_received = sess.receive(data_received)
    data_received = pres.receive(data_received)
    data_received = app.receive(data_received)

    print("\nReceived Message:", data_received)