
import streamlit as st
import openai
import os

# Set OpenAI API key
openai.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

def generate_revision(draft, tone, fixes, keep_avoid):
    prompt = (
        f"Here’s an email draft:\n\n{draft}\n\n"
        f"Please rewrite it in a {tone} tone, "
        f"focusing on: {', '.join(fixes)}."
    )
    if keep_avoid:
        prompt += f"\n\nMaintain or avoid: {keep_avoid}."
    prompt += "\n\nProvide only the improved version."

    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def generate_subject(draft, tone):
    prompt = f"Suggest a clear, attention-grabbing email subject line in a {tone} tone based on this message:\n\n{draft}"
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

st.title("✉️ Email Polisher")

draft = st.text_area("Paste your email draft here", height=200)
tone = st.selectbox("Choose a tone", ["Professional", "Friendly", "Conversational", "Direct", "Casual", "Custom"])
if tone == "Custom":
    tone = st.text_input("Specify custom tone", value="")
fixes = st.multiselect("Fixes to apply", 
                       ["Grammar & spelling", "Shorten/concise", "Reword for tone", "Make more natural", "Make more formal"])
keep_avoid = st.text_input("Phrases to keep or avoid (optional)", placeholder="e.g. don’t say ‘love’; keep mention of internship")
generate_subj = st.checkbox("Generate subject line?", value=True)

if st.button("Polish Email"):
    if not draft.strip():
        st.error("Please paste an email draft before polishing.")
    else:
        with st.spinner("Rewriting your email..."):
            improved = generate_revision(draft, tone, fixes, keep_avoid)
            st.subheader("🔄 Improved Email")
            st.write(improved)
        if generate_subj:
            with st.spinner("Generating subject line..."):
                subj = generate_subject(draft, tone)
                st.subheader("📧 Suggested Subject Line")
                st.write(subj)
