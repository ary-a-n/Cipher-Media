import streamlit as st
import cv2
import numpy as np
import base64
from Steno import img_encoder, img_decoder, audio_encode, decode_audio, encode_vid_data, decode_vid_data

st.title("CipherMedia")

option = st.sidebar.selectbox("Choose an option", ["Image", "Audio", "Video"])

if option == "Image":
    st.header("Image Steganography")
    action = st.sidebar.selectbox("Choose an action", ["Encode", "Decode"])

    if action == "Encode":
        st.subheader("Encode Data in Image")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        data = st.text_input("Enter the data to be encoded in the image")
        file_name = st.text_input("Enter the name of the New Image (Stego Image) after Encoding:")

        if st.button("Encode"):
            if uploaded_image is not None and data:
                try:
                    image = np.array(cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR))
                    encoded_image = img_encoder(image, data)
                    st.image(encoded_image, caption='Encoded Image', use_column_width=True)

                    result = cv2.imencode('.png', encoded_image)[1].tobytes()
                    st.download_button(label="Download Encoded Image", data=result, file_name=file_name, mime="image/png")
                except ValueError as e:
                    st.error(e)
            else:
                st.error("Please upload an image and enter data to encode.")

    elif action == "Decode":
        st.subheader("Decode Data from Image")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        if st.button("Decode"):
            if uploaded_image is not None:
                try:
                    image = np.array(cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR))
                    decoded_data = img_decoder(image)
                    if decoded_data:
                        st.success(f"The encoded data is: {decoded_data}")
                    else:
                        st.error("No data found or image is corrupted.")
                except ValueError as e:
                    st.error(e)
elif option == "Audio":
    st.header("Audio Steganography")
    action = st.sidebar.selectbox("Choose an action", ["Encode", "Decode"])

    if action == "Encode":
        st.subheader("Encode Data in Audio")
        uploaded_audio = st.file_uploader("Upload an audio file", type=["wav"])
        data = st.text_input("Enter the data to be encoded in the audio")
        output_file_name = st.text_input("Enter the name of the output file (Stego Audio) after Encoding:")

        if st.button("Encode"):
            if uploaded_audio is not None and data:
                try:
                    # Save the uploaded audio file temporarily
                    temp_audio_path = "temp_audio_file.wav"  # Assuming WAV format for simplicity

                    with open(temp_audio_path, "wb") as f:
                        f.write(uploaded_audio.read())

                    # Encode data into audio
                    audio_encode(temp_audio_path, output_file_name, data)

                    st.success("Audio encoded successfully!")

                    # Provide a download link for the stego audio file
                    with open(output_file_name, "rb") as f:
                        bytes = f.read()
                    b64 = base64.b64encode(bytes).decode()
                    href = f'<a href="data:file/wav;base64,{b64}" download="{output_file_name}">Download encoded Audio</a>'
                    st.markdown(href, unsafe_allow_html=True)

                    # Optionally, play the stego audio directly
                    st.audio(output_file_name, format='audio/wav')

                except Exception as e:
                    st.error(f"Error encoding audio: {e}")
            else:
                st.error("Please upload an audio file and enter data to encode.")

    elif action == "Decode":
        st.subheader("Decode Data from Audio")
        uploaded_audio_decode = st.file_uploader("Upload stego audio file", type=["wav"])

        if st.button("Decode"):
            if uploaded_audio_decode is not None:
                try:
                    # Save the uploaded audio file temporarily
                    temp_audio_path = "temp_audio_file.wav"  # Assuming WAV format for simplicity

                    with open(temp_audio_path, "wb") as f:
                        f.write(uploaded_audio_decode.read())

                    # Decode data from audio
                    decoded_data = decode_audio(temp_audio_path)

                    st.text("Decoded Data:")
                    st.write(decoded_data)

                except Exception as e:
                    st.error(f"Error decoding audio: {e}")
            else:
                st.error("Please upload an audio file to decode.")

elif option == "Video":
    st.header("Video Steganography")
    action = st.sidebar.selectbox("Choose an action", ["Encode", "Decode"])

    if action == "Encode":
        st.subheader("Encode Data in Video")
        uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi"])
        data = st.text_input("Enter the data to be encoded in the video")
        output_file_name = st.text_input("Enter the name of the output video file (Stego Video) after Encoding:")
        frame_number = st.number_input("Enter the frame number where you want to embed data:", min_value=1, step=1)
        encryption_key = st.text_input("Enter encryption key:")

        if st.button("Encode"):
            if uploaded_video is not None and data and output_file_name and frame_number and encryption_key:
                try:
                    # Save the uploaded video file temporarily
                    temp_video_path = "temp_video_file.mp4"  # Assuming MP4 format for simplicity

                    with open(temp_video_path, "wb") as f:
                        f.write(uploaded_video.read())

                    frame = encode_vid_data(temp_video_path, output_file_name, frame_number, data, encryption_key)

                    st.success("Video encoded successfully!")

                    # Provide a download link for the stego video file
                    with open(output_file_name, "rb") as f:
                        bytes = f.read()
                    st.download_button(label="Download Stego Video", data=bytes, file_name=output_file_name, mime="video/mp4")

                except Exception as e:
                    st.error(f"Error encoding video: {e}")

            else:
                st.error("Please upload a video file, enter data to encode, specify a frame number, and enter an encryption key.")

    elif action == "Decode":
        st.subheader("Decode Data from Video")
        uploaded_video_decode = st.file_uploader("Upload stego video file", type=["mp4", "avi"])
        frame_number_decode = st.number_input("Enter the frame number from where you want to extract data:", min_value=1, step=1)
        decryption_key = st.text_input("Enter decryption key:")

        if st.button("Decode"):
            if uploaded_video_decode is not None and frame_number_decode and decryption_key:
                try:
                    # Save the uploaded video file temporarily
                    temp_video_path = "temp_video_file.mp4"  # Assuming MP4 format for simplicity

                    with open(temp_video_path, "wb") as f:
                        f.write(uploaded_video_decode.read())

                    decoded_data = decode_vid_data(temp_video_path, frame_number_decode, decryption_key)

                    st.text("Decoded Data:")
                    st.write(decoded_data)

                except Exception as e:
                    st.error(f"Error decoding video: {e}")

            else:
                st.error("Please upload a video file, specify a frame number, and enter a decryption key.")


