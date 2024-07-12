# CipherMedia

### Tech Stack and Libraries Used

- **Tech Stack**: Python, Streamlit
- **Libraries**: OpenCV-python, Pillow, NumPy
  
**Steganography** is the practice of concealing communication by embedding information within other data. This project enables users to hide secret messages within image, text, audio, and video files. The sender selects a cover file (image, audio, or video), embeds a secret text using efficient algorithms, and generates a stego file of the same format as the cover file. This stego file can then be transmitted via private or public communication networks. At the receiver's end, the stego file is downloaded and decoded using the appropriate algorithm to retrieve the hidden text.

![Cover Image](https://user-images.githubusercontent.com/77832407/152796278-a60d3042-a6cd-442d-96e0-7f5a8b11f3ed.jpg)

## Image Steganography (Hiding TEXT in IMAGE)

In image steganography, the project employs the Least Significant Bit Insertion technique to overwrite the least significant bit of each pixel's color channels (Red, Green, Blue) with bits from the text message characters. A delimiter is appended to the end of the text message to mark the completion of the message, which aids in the decoding process.

## Audio Steganography

Audio Steganography is a technique used to hide secret messages within audio files. In this project, we use a method called the Least Significant Bit (LSB) Algorithm to embed text into audio files.

### Encoding Process

1. **Frame Conversion**: Each byte of the audio file is converted into an 8-bit format.

2. **LSB Modification**: For each frame byte:
   - We check the 4th Least Significant Bit (LSB) to see if it matches the secret message bit.
   - If the LSB matches, we change the 2nd LSB to 0 using a logical AND operation with 253 (11111101).
   - If the LSB doesn't match, we change the 2nd LSB to 1 using a logical AND operation with 253, followed by a logical OR operation to set it to 1.
   
3. **Embedding**: The secret message bit is then embedded into the LSB of each frame byte. This is done using a logical AND operation between the frame byte and a binary number of 254 (11111110), followed by a logical OR operation with the next bit (0 or 1) from the secret message.

### Decoding Process

The decoding process reverses the encoding steps to extract the hidden message from the audio file.

### Usage

Audio Steganography allows for covert communication by hiding information within seemingly normal audio files, making it suitable for secure data transmission and embedding metadata without altering the audio's perceptual quality.

## Video Steganography

Video Steganography is a technique used to conceal secret messages within video files. In this project, we combine cryptography and steganography for secure message embedding.

### Encryption Process

1. **RC4 Encryption**: 
   - **Key-Scheduling Algorithm (KSA)**: Initialize a list `S` of length 256 and set it to values 0 to 255 in ascending order. Permute `S` based on a user-provided key converted into ASCII values.
   - **Pseudo-Random Generation Algorithm (PRGA)**: Generate a keystream byte sequence of the same length as the plaintext by iterating through `S`, swapping values, and using XOR operations.

2. **Encoding**:
   - Convert plaintext to ciphertext using the RC4 keystream obtained.
   - Embed the ciphertext into the video frames.

### Embedding Process

1. **Ciphertext Embedding**: 
   - For each frame in the video:
     - Convert pixel values to binary.
     - Modify the Least Significant Bit (LSB) of pixel values to encode binary digits of the ciphertext.
     - Ensure imperceptibility to maintain video quality.

2. **Steganographic Security**:
   - Distribute ciphertext across multiple frames for enhanced security.
   - Use robust embedding techniques to resist detection.

### Decryption Process

1. **RC4 Decryption**:
   - Use the same key and algorithms (KSA and PRGA) to generate the same keystream used for encryption.
   - XOR the ciphertext from the video frames with the keystream to retrieve the plaintext.

### Usage

Video Steganography provides covert communication capabilities by concealing sensitive information within video files. It ensures data security and confidentiality during transmission and storage, making it suitable for applications requiring hidden data exchange and digital watermarking without compromising video quality.
