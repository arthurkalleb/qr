import cv2
from pyzbar.pyzbar import decode
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.video_capture = cv2.VideoCapture('video.mp4')
        self.overlay_active = False
        self.video_frame = None

    def read_video_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_capture.read()
        return frame

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            (x, y, w, h) = obj.rect
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            self.overlay_active = True

        if self.overlay_active:
            self.video_frame = self.read_video_frame()
            img = self.overlay_video(img, self.video_frame, x, y, w, h)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def overlay_video(self, frame, video_frame, x, y, w, h):
        video_frame = cv2.resize(video_frame, (w, h))
        frame[y:y+h, x:x+w] = video_frame
        return frame

def main():
    st.title("Magipix-like AR with Streamlit")
    st.write("Scan a QR code to see the AR video overlay.")

    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if __name__ == "__main__":
    main()
