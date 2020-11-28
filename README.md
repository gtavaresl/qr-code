# qr-code

Project repository presented for the second week of Coding Week, whose theme is visual recognition. It is the implementation of a QR Code detector and decoder using the pyzbar lib. Different application codes are presented.

## Repository Description

- ```code```: Folder containing the codes used in the project.
- ```code/QRpackage```: Contain the QRdecode.py module, which implements the QR code detector and decoder.
- ```code/image-qrcode.py```: Implements processing for a single image.
- ```code/sequential-video.py```: Implements the processing for an incoming video, sequentially.
- ```code/threading-video.py```: Implements the processing of an incoming video, in parallel. An advanced version of the sequential.
- ```code/client.py and server.py```: Implements a socket between server and client, the client being the source of the video and the server decodes QR codes in the frames, returning it to the client.

## Requirements

- Python 3 interpreter
- Install the libs at: ```requirements.txt``` (file generated using the pipreqs tool)
