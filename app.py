import cv2
import qreader
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.overlay_active = False
        self.video_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        detector = qreader.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = detector(img)

        if retval:
            for info in decoded_info:
                print(f"QR Code Data: {info}")
                self.overlay_active = True

        if self.overlay_active:
            # Simulate overlay logic here if needed
            pass

        return av.VideoFrame.from_ndarray(img, format="bgr24")


def main():
    st.title("Magipix-like AR with Streamlit")
    st.write("Scan a QR code to see the AR video overlay.")

    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)


if __name__ == "__main__":
    main()
