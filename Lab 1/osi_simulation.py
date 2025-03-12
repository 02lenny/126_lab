import json
import struct
import pickle

# Physical Layer
class PhysicalLayer:
    def send(self, data):
        encoded = data.hex()
        print("[Physical] Sending raw data:", encoded)
        return encoded.encode()

    def receive(self, data):
        decoded = bytes.fromhex(data.decode())
        print("[Physical] Received raw data (decoded):", decoded)
        return decoded

# Data Link Layer
class DataLinkLayer:
    def send(self, data, mac_address):
        framed_data = f"MAC_HEADER:{mac_address}|".encode() + data
        print("[Data Link] Framed Data:", framed_data)
        return framed_data

    def receive(self, data):
        header, stripped_data = data.split(b'|', 1)
        print("[Data Link] Received Data:", stripped_data)
        return stripped_data

# Network Layer
class NetworkLayer:
    def send(self, data, ip_address):
        packet = f"IP_HEADER:{ip_address}|".encode() + data
        print("[Network] Routed Packet:", packet)
        return packet

    def receive(self, data):
        header, stripped_packet = data.split(b'|', 1)
        print("[Network] Received Packet:", stripped_packet)
        return stripped_packet

# Transport Layer
class TransportLayer:
    def send(self, data):
        segment = struct.pack('>I', len(data)) + data
        print("[Transport] Segment Data:", segment)
        return segment

    def receive(self, data):
        length = struct.unpack('>I', data[:4])[0]
        reassembled_data = data[4:]
        print(f"[Transport] Reassembled Data (SEQ {length}):", reassembled_data)
        return reassembled_data

# Session Layer
class SessionLayer:
    def send(self, data):
        session_data = json.dumps({"session": "open", "data": data.hex()}).encode()
        print("[Session] Session Opened:", session_data)
        return session_data

    def receive(self, data):
        session_info = json.loads(data.decode())
        stripped = bytes.fromhex(session_info["data"])
        print("[Session] Session Data:", stripped)
        return stripped

# Presentation Layer
class PresentationLayer:
    def send(self, data):
        encoded_data = pickle.dumps(data)
        print("[Presentation] Encoded Data:", encoded_data)
        return encoded_data

    def receive(self, data):
        decoded_data = pickle.loads(data)
        print("[Presentation] Decoded Data:", decoded_data)
        return decoded_data

# Application Layer
class ApplicationLayer:
    def send(self, data):
        request = f"HTTP_REQUEST:{data}".encode()
        print("[Application] Sending Request:", request)
        return request

    def receive(self, data):
        response = data.replace(b"HTTP_REQUEST:", b"HTTP_RESPONSE:OK ")
        print("[Application] Received Response:", response)
        return response

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

    print("\n--- RECEIVING DATA ---\n")
    data_received = phys.receive(phys_data)
    data_received = data_link.receive(data_received)
    data_received = net.receive(data_received)
    data_received = trans.receive(data_received)
    data_received = sess.receive(data_received)
    data_received = pres.receive(data_received)
    data_received = app.receive(data_received)

    print("\nReceived Message:", data_received.decode())