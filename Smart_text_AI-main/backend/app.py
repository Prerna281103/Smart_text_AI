import streamlit as st
import requests
from services.home import home_page  
from services.summarize_text import summarize_text_page, extract_text_from_pdf, extract_text_from_docx

st.set_page_config(page_title="AI Document Processor", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.sidebar.title("🔍 Features")
selected_function = st.sidebar.radio(
    "Select Functionality:",
    ["🏠 Home", "📂 Extract Text", "📑 Summarize Text", "🌎 Translate Text", "🔠 Transliteration", "🖼️ Extract Images", "❓ Q&A"]
)

# Load Home Page
if selected_function == "🏠 Home":
    home_page()

# File upload helper function
# Update the upload_file_and_post helper function
def upload_file_and_post(endpoint: str, file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    # Ensure all endpoints use the /api prefix
    if not endpoint.startswith('api/'):
        endpoint = f"api/{endpoint}"
    response = requests.post(f"{API_URL}/{endpoint}", files=files)
    return response

# Update the endpoints in your function calls
# For Summarize Text section
if selected_function == "📑 Summarize Text":
    st.title("Summarize Text from Documents")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file and st.button("Summarize"):
        with st.spinner("Summarizing text..."):
            try:
                response = upload_file_and_post("summarize-text", uploaded_file)
                if response.status_code == 200:
                    summary = response.json().get("summary", "")
                    st.text_area("Summary:", summary, height=300)
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Failed to summarize text: {error_detail}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Translate Text
# Translate Text
if selected_function == "🌎 Translate Text":
    st.title("Translate Text from Documents")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])
    text_input = st.text_area("Enter text to translate:")

    target_language = st.selectbox("Select Target Language", [
        "Hindi", "Marathi", "Tamil", "Telugu", "Gujarati", "Bengali", "Kannada", "Punjabi", "French", "Spanish"
    ])

    if st.button("🌍 Translate"):
        with st.spinner("Translating..."):
            try:
                if uploaded_file:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {
                        "target_language": target_language.lower(),
                        "file_upload": "true"
                    }
                    response = requests.post(f"{API_URL}/api/translate/", files=files, data=data)
                elif text_input.strip():
                    data = {
                        "text": text_input,
                        "target_language": target_language.lower(),
                        "file_upload": "false"
                    }
                    response = requests.post(f"{API_URL}/api/translate/", data=data)
                else:
                    st.warning("⚠ Please upload a file or enter text to translate.")
                    response = None
                    
                if response and response.status_code == 200:
                    translated_text = response.json().get("translated_text", "Translation failed!")
                    st.text_area("Translated Text:", translated_text, height=300)
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download Translation",
                        data=translated_text,
                        file_name="translated_text.txt",
                        mime="text/plain"
                    )
                elif response:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Translation failed: {error_detail}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Transliteration
# Transliteration
if selected_function == "🔠 Transliteration":
    st.title("Transliterate Text")
    input_method = st.radio("Choose Input Method:", ["Upload Document", "Enter Text"])
    target_script = st.selectbox(
        "Select Target Script",
        ["Devanagari (Hindi/Sanskrit)", 
         "Bengali (Bangla)", 
         "Gujarati",
         "Gurmukhi (Punjabi)",
         "Kannada",
         "Malayalam",
         "Odia (Oriya)",
         "Tamil",
         "Telugu",
         "Urdu",
         "Latin",
         "Arabic",
         "Chinese",
         "Japanese",
         "Korean",
         "Cyrillic",
         "Greek"]
    )

    # Upload Document Option
    if input_method == "Upload Document":
        uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])
        if uploaded_file and target_script and st.button("Transliterate"):
            with st.spinner("Transliterating..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {
                        "target_script": target_script,
                        "file_upload": "true"
                    }
                    response = requests.post(f"{API_URL}/api/transliterate/", files=files, data=data)
                    if response.status_code == 200:
                        transliterated_text = response.json().get("transliterated_text", "")
                        st.text_area("Transliterated Text:", transliterated_text, height=300)
                        
                        # Add download button
                        st.download_button(
                            label="📥 Download Transliterated Text",
                            data=transliterated_text,
                            file_name="transliterated_text.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Transliteration failed: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Enter Text Option
    else:
        text_to_transliterate = st.text_area("Enter text to transliterate:", height=200)
        if text_to_transliterate and target_script and st.button("Transliterate"):
            with st.spinner("Transliterating..."):
                try:
                    data = {
                        "text": text_to_transliterate,
                        "target_script": target_script,
                        "file_upload": "false"
                    }
                    response = requests.post(f"{API_URL}/api/transliterate/", data=data)
                    if response.status_code == 200:
                        transliterated_text = response.json().get("transliterated_text", "")
                        st.text_area("Transliterated Text:", transliterated_text, height=300)

                        # Add download button
                        st.download_button(
                            label="📥 Download Transliterated Text",
                            data=transliterated_text,
                            file_name="transliterated_text.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Transliteration failed: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
# Extract Text section
if selected_function == "📂 Extract Text":
    st.title("Extract Text from Documents")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file:
        response = upload_file_and_post("extract-text", uploaded_file)
        if response.status_code == 200:
            extracted_text = response.json().get("extracted_text", "")
            st.text_area("Extracted Text:", extracted_text, height=300)
            
            # Add download button
            st.download_button(
                label="📥 Download Extracted Text",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.error("Failed to extract text!")

# After Extract Text section, add:

# Extract Images
# In the Extract Images section, update the image display code
if selected_function == "🖼️ Extract Images":
    st.title("Extract Images from Documents")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf"])

    if uploaded_file and st.button("Extract Images"):
        try:
            with st.spinner("Extracting images..."):
                response = upload_file_and_post("extract-images", uploaded_file)
                
                if response.status_code == 200:
                    images = response.json().get("images", [])
                    if images:
                        st.success(f"Found {len(images)} images!")
                        cols = st.columns(3)
                        for idx, img_base64 in enumerate(images):
                            with cols[idx % 3]:
                                try:
                                    st.image(
                                        img_base64,
                                        caption=f"Image {idx+1}",
                                        use_container_width=True  # Updated from use_column_width
                                    )
                                except Exception as img_error:
                                    st.error(f"Error displaying image {idx+1}")
                        
                        # Create download buttons for individual images and ZIP file
                        st.markdown("### Download Options")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Download individual images
                            for idx, img_base64 in enumerate(images):
                                try:
                                    import base64
                                    from io import BytesIO
                                    
                                    # Convert base64 to bytes
                                    if "base64," in img_base64:
                                        img_base64 = img_base64.split("base64,")[1]
                                    img_bytes = base64.b64decode(img_base64)
                                    
                                    st.download_button(
                                        label=f"Download Image {idx+1}",
                                        data=img_bytes,
                                        file_name=f"extracted_image_{idx+1}.png",
                                        mime="image/png"
                                    )
                                except Exception as e:
                                    st.error(f"Error creating download button for image {idx+1}")
                        
                        with col2:
                            # Download all images as ZIP
                            try:
                                import zipfile
                                zip_buffer = BytesIO()
                                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                    for idx, img_base64 in enumerate(images):
                                        if "base64," in img_base64:
                                            img_base64 = img_base64.split("base64,")[1]
                                        img_bytes = base64.b64decode(img_base64)
                                        zip_file.writestr(f"extracted_image_{idx+1}.png", img_bytes)
                                
                                st.download_button(
                                    label="Download All Images (ZIP)",
                                    data=zip_buffer.getvalue(),
                                    file_name="extracted_images.zip",
                                    mime="application/zip"
                                )
                            except Exception as e:
                                st.error("Error creating ZIP file for download")
                    else:
                        st.info("No images found in the document.")
                else:
                    st.error(f"Failed to extract images. Status: {response.status_code}")
                    if response.text:
                        st.error(f"Error details: {response.text}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")

# Q&A
if selected_function == "❓ Q&A":
    st.title("Ask Questions About Your Document")
    
    input_method = st.radio("Choose Input Method:", ["Upload Document", "Enter Text"])
    
    if input_method == "Upload Document":
        uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])
        if uploaded_file:
            question = st.text_input("Enter your question about the document:")
            if st.button("Get Answer") and question:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"question": question}
                try:
                    response = requests.post(f"{API_URL}/api/qna", files=files, data=data)
                    if response.status_code == 200:
                        answer = response.json().get("answer")
                        if answer:
                            st.markdown("### Answer:")
                            st.markdown(answer)
                            
                            # Add download button
                            full_qa_text = f"Question:\n{question}\n\nAnswer:\n{answer}"
                            st.download_button(
                                label="📥 Download Q&A",
                                data=full_qa_text,
                                file_name="qa_response.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error("No answer received from the model.")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error occurred')}")
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
    else:
        context = st.text_area("Enter your text context:", height=200, 
                             help="Paste the text you want to ask questions about")
        question = st.text_input("Enter your question:", 
                               help="Ask a specific question about the text above")
        
        if st.button("Get Answer") and context and question:
            try:
                response = requests.post(
                    f"{API_URL}/api/qna", 
                    json={
                        "text": context,
                        "question": question
                    }
                )
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    if answer:
                        st.markdown("### Answer:")
                        st.markdown(answer)
                    else:
                        st.error("No answer received from the model.")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error occurred')}")
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")