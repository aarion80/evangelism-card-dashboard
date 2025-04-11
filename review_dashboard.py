import streamlit as st
import json
import os
from PIL import Image

# CONFIG
MESSAGE_JSON = "sample_evangelism_messages.json"
IMAGE_DIR = "image"

# Load messages
if os.path.exists(MESSAGE_JSON):
    with open(MESSAGE_JSON, "r") as f:
        messages = json.load(f)
else:
    messages = []

st.title("📖 Evangelism Message Review Dashboard")

# For editing session state
if 'edited' not in st.session_state:
    st.session_state.edited = {}

# Display all messages
for msg in messages:
    with st.expander(f"✍️ Message #{msg['id']}: {msg.get('title', 'Untitled')}"):
        st.markdown("### Quote")
        new_text = st.text_area("Hook/Headline", value=msg['text'], key=f"text_{msg['id']}")

        st.markdown("### Reflection")
        new_reflection = st.text_area("Pastoral Reflection", value=msg.get('reflection', ''), key=f"reflection_{msg['id']}")

        st.markdown("### Scripture Reference")
        new_verse = st.text_input("Verse", value=msg['verse'], key=f"verse_{msg['id']}")

        image_path = os.path.join(IMAGE_DIR, msg.get("image", ""))
        if os.path.exists(image_path):
            st.image(image_path, caption=msg['image'], use_column_width=True)
        else:
            st.warning("Image not found.")

        approved = st.checkbox("✅ Approve this message", value=msg.get("approved", False), key=f"approve_{msg['id']}")

        # Store edits in session state
        st.session_state.edited[msg['id']] = {
            "text": new_text,
            "reflection": new_reflection,
            "verse": new_verse,
            "approved": approved
        }

# Save changes button
if st.button("💾 Save All Changes"):
    for msg in messages:
        edits = st.session_state.edited.get(msg['id'])
        if edits:
            msg['text'] = edits['text']
            msg['reflection'] = edits['reflection']
            msg['verse'] = edits['verse']
            msg['approved'] = edits['approved']

    with open(MESSAGE_JSON, "w") as f:
        json.dump(messages, f, indent=2)
    st.success("Changes saved successfully!")

