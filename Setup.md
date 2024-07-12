# Setup Guide for CipherMedia

## Prerequisites

Before running the CipherMedia Steganography App, ensure you have the following installed:
- Python (version 3.7 or higher recommended)
- Git (optional, for cloning the repository)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ary-a-n/Cipher-Media.git
   cd Cipher-Media
   ```
2. **Setup Virtual Environment (Optional but Recommended):**
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
    pip install -r requirements.txt
   ```
## Running the Application
  ```python
  streamlit run app.py
  ```
## Using CipherMedia

1. **Choose an Option**: Select either Image, Audio, or Video from the sidebar based on your data type.

2. **Select Action**: Choose Encode or Decode depending on whether you want to hide or retrieve data.

3. **Upload Files and Input Data**: Follow on-screen instructions to upload your file(s) and input the data to be encoded or decoded.

4. **Interact with the App**: Navigate through the app interface to perform your desired action.

5. **Download or View**: After encoding or decoding, download the encoded files or view the decoded messages.

### Additional Notes

- Ensure files are in supported formats before uploading:
  - Images: PNG, JPG, JPEG
  - Audio: WAV
  - Video: MP4

This setup ensures smooth usage of the Cipher-Media App, allowing for secure data hiding and retrieval within supported file types.



   
