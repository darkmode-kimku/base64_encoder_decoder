#!/bin/bash
pyinstaller --icon=icon.ico --onefile --add-data="icon.ico;." -F -w base64_decode_qt.py -n BASE64_Encoder_Decoder.exe