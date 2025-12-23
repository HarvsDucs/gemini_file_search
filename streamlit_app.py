
import streamlit as st
import os
import time
import tempfile
from google import genai
from google.genai import types

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini File Search Manager",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styles ---
st.markdown("""
<style>
    /* Force generic dark text */
    .stApp, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #000000 !important;
    }
    .stApp {
        background-color: #ffffff;
    }
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
    }
    /* Light theme expander */
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #ffffff;
    }
    /* Ensure input text is visible and matches theme */
    .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialization ---
# --- Initialization ---
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GOOGLE_API_KEY")

@st.cache_resource
def get_client(api_key):
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing client: {e}")
        return None

client = get_client(st.session_state.api_key)

# --- Sidebar ---
st.sidebar.title("💎 Gemini Manager")
st.sidebar.markdown("---")

if not client:
    st.sidebar.warning("API Key not found!")
    api_key_input = st.sidebar.text_input("Enter Google API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.rerun()
    st.stop()

# --- Pricing & Limits Sidebar ---
with st.sidebar.expander("💰 Pricing & Limits", expanded=False):
    st.markdown("""
    **Pricing**
    - **Indexing**: Charged as embeddings ($0.15 per 1M tokens)
    - **Storage**: Free 
    - **Query Embeddings**: Free
    - **Context**: Retrieved tokens charged as regular input
    
    **Limits (Total Project Size)**
    - **Free**: 1 GB
    - **Tier 1**: 10 GB
    - **Tier 2**: 100 GB
    - **Tier 3**: 1 TB
    
    *Max file size: 100 MB*
    *Rec. Store Size: < 20 GB*
    """)


# --- Functions ---

def list_stores():
    try:
        return list(client.file_search_stores.list())
    except Exception as e:
        st.error(f"Error fetching stores: {e}")
        return []

def create_new_store(name):
    try:
        return client.file_search_stores.create(config={'display_name': name})
    except Exception as e:
        st.error(f"Error creating store: {e}")
        return None

def delete_existing_store(store_name):
    try:
        client.file_search_stores.delete(name=store_name, config={'force': True})
        return True
    except Exception as e:
        st.error(f"Error deleting store: {e}")
        return False

def upload_files_to_store(files, store_name, chunk_size=None, chunk_overlap=None):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(files)
    
    # helper to construct config if needed
    upload_config = {'display_name': ''}
    
    for idx, file in enumerate(files):
        status_text.text(f"Processing {file.name}...")
        
        # Save to temp file because SDK expects a path
        suffix = os.path.splitext(file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
            
        try:
            # Prepare config per file
            current_config = {'display_name': file.name}
            
            # Add chunking config if provided
            if chunk_size is not None and chunk_overlap is not None:
                current_config['chunking_config'] = {
                    'white_space_config': {
                        'max_tokens_per_chunk': chunk_size,
                        'max_overlap_tokens': chunk_overlap
                    }
                }

            op = client.file_search_stores.upload_to_file_search_store(
                file=tmp_path,
                file_search_store_name=store_name,
                config=current_config
            )
            # Wait for completion
            while not op.done:
                time.sleep(1)
                op = client.operations.get(op)
                
            results.append(f"✅ {file.name}")
        except Exception as e:
            results.append(f"❌ {file.name}: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        progress_bar.progress((idx + 1) / total_files)
        
    status_text.empty()
    progress_bar.empty()
    return results

def query_store(store_name, query_text):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query_text,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )
        return response
    except Exception as e:
        st.error(f"Error querying store: {e}")
        return None

# --- Main Interface ---

st.title("📂 File Store Management")
st.markdown("Manage your Gemini File Stores, upload documents, and prepare your specialized knowledge bases.")

# Stores Section
stores = list_stores()

col1, col2 = st.columns([3, 1])
with col2:
    st.subheader("Create Store")
    with st.form("create_store_form"):
        new_store_name = st.text_input("Store Display Name", placeholder="e.g. Finance Docs")
        submitted = st.form_submit_button("Create New Store", type="primary")
        if submitted and new_store_name:
            with st.spinner("Creating..."):
                store = create_new_store(new_store_name)
                if store:
                    st.toast(f"Store '{store.display_name}' created!", icon="🎉")
                    time.sleep(1)
                    st.rerun()

with col1:
    st.subheader(f"Your File Stores ({len(stores)})")
    
    if not stores:
        st.info("No file stores found. Create one to get started.")
    
    for store in stores:
        with st.expander(f"**{store.display_name}**  `{store.name}`", expanded=False):
            
            # Create tabs for different actions
            tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "💬 Chat & Search", "⚙️ Settings"])
            
            with tab1:
                st.markdown("#### Upload Documents")
                
                # Chunking Configuration
                with st.expander("Advanced: Chunking Configuration"):
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        chunk_size = st.number_input(
                            "Max Tokens per Chunk", 
                            min_value=100, 
                            max_value=2048, 
                            value=None, 
                            step=100,
                            key=f"chunk_size_{store.name}",
                            help="Leave empty for default"
                        )
                    with c_col2:
                        chunk_overlap = st.number_input(
                            "Max Overlap Tokens", 
                            min_value=0, 
                            max_value=500, 
                            value=None, 
                            step=10,
                            key=f"chunk_overlap_{store.name}",
                            help="Leave empty for default"
                        )

                uploaded_files = st.file_uploader(
                    "Drop files here", 
                    accept_multiple_files=True, 
                    key=f"uploader_{store.name}"
                )
                
                if uploaded_files:
                    if st.button(f"Start Upload ({len(uploaded_files)} files)", key=f"btn_{store.name}"):
                        with st.spinner("Uploading files to Gemini..."):
                            # Filter None values for chunking
                            cs = int(chunk_size) if chunk_size else None
                            co = int(chunk_overlap) if chunk_overlap else None
                            
                            logs = upload_files_to_store(uploaded_files, store.name, cs, co)
                            for log in logs:
                                st.write(log)
                        st.success("Upload batch completed.")

            with tab2:
                st.markdown("#### Ask questions about your documents")
                query = st.text_input("Enter your query", key=f"query_{store.name}")
                if st.button("Search", key=f"search_{store.name}", type="primary"):
                    if query:
                        with st.spinner("Thinking..."):
                            response = query_store(store.name, query)
                            if response:
                                st.markdown("### Answer")
                                st.write(response.text)
                                
                                # Process Citations
                                if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.grounding_chunks:
                                    st.markdown("---")
                                    st.markdown("### � Citations")
                                    
                                    # We need to process the grounding_metadata
                                    # The structure is usually response.candidates[0].grounding_metadata.grounding_chunks
                                    # which contains the content or uri, and supports contains indices
                                    
                                    metadata = response.candidates[0].grounding_metadata
                                    
                                    # Just raw dump for inspection if needed, or structured display
                                    # st.json(metadata.to_dict()) # Debug
                                    
                                    for idx, chunk in enumerate(metadata.grounding_chunks):
                                        if hasattr(chunk, 'retrieved_context'):
                                            rc = chunk.retrieved_context
                                            title = rc.title if rc.title else f"Source {idx+1}"
                                            uri = rc.uri
                                            
                                            with st.expander(f"Citation {idx+1}: {title}"):
                                                st.caption(f"URI: {uri}")
                                                
                                                # Try to display text content if available in the metadata
                                                context_text = None
                                                # Check typical fields where text might be hidden
                                                if hasattr(rc, 'text') and rc.text:
                                                    context_text = rc.text
                                                elif hasattr(rc, 'parts') and rc.parts:
                                                     # If parts is a list of objects with text
                                                    context_text = "\\n".join([p.text for p in rc.parts if hasattr(p, 'text') and p.text])
                                                
                                                if context_text:
                                                    st.markdown(f"**Excerpt:**")
                                                    st.info(context_text)
                                                else:
                                                    st.write("No text snippet found in metadata.")
                                                
                                                # Debug: Show full raw data so user can inspect structure
                                                with st.popover("Inspect Raw Metadata"):
                                                    try:
                                                        st.json(chunk.model_dump())
                                                    except AttributeError:
                                                        st.write(chunk)
                                else:
                                    st.info("No specific citations found for this answer.")

            with tab3:
                st.markdown("#### Store Settings")
                st.write(f"**Store ID:** `{store.name}`")
                st.write(f"**Created At:** {store.create_time}")
                
                st.markdown("---")
                if st.button("🗑️ Delete Store", key=f"del_{store.name}", type="secondary"):
                    with st.spinner("Deleting..."):
                        if delete_existing_store(store.name):
                            st.toast("Store deleted successfully.", icon="🗑️")
                            time.sleep(1)
                            st.rerun()

# Footer
st.markdown("---")
st.caption("Gemini File Search Manager | Powered by Streamlit & Google Gen AI")
