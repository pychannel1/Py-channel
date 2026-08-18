import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Burmese Movie Recap Generator", page_icon="")

st.title("Burmese Movie Recap Generator")
st.write("ဇာတ်လမ်း အကျဉ်း သို့မဟုတ် အကြောင်းအရာကို ထည့်သွင်းပေးပါ။")

# API Key ရယူခြင်း
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key မတွေ့ပါ။ Settings တွင် GEMINI_API_KEY ထည့်ပေးပါ။")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# User စာရိုက်ထည့်ရမည့် နေရာ
user_input = st.text_area("ဇာတ်လမ်း အကြောင်းအရာ ရိုက်ထည့်ပါ-", placeholder="ဒီနေရာမှာ ဇာတ်လမ်းအကျဉ်းကို ရိုက်ထည့်ပါ...")

if st.button("Generate Recap", type="primary"):
    if not user_input.strip():
        st.warning("ကျေးဇူးပြု၍ စာသား အရင် ရိုက်ထည့်ပေးပါ။")
    else:
        with st.spinner("AI က Movie Recap ရေးသားနေပါသည်..."):
            try:
                prompt = f"""
                သင်သည် ကျွမ်းကျင်သော Burmese Movie Recapper တစ်ဦး ဖြစ်သည်။
                အောက်ပါ ဇာတ်လမ်းအချက်အလက်ကို အခြေခံပြီး စိတ်ဝင်စားဖွယ် Movie Recap တစ်ခု ရေးပေးပါ:

                {user_input}
                """
                response = model.generate_content(prompt)
                st.success("အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ!")
                st.markdown("### ရလဒ်:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
