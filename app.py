import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Burmese Movie Recap Generator", page_icon="")

st.title("Burmese Movie Recap Generator")
st.write("ဇာတ်လမ်း အကျဉ်း သို့မဟုတ် အကြောင်းအရာကို ထည့်သွင်းပေးပါ။")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key မတွေ့ပါ။ Settings တွင် GEMINI_API_KEY ထည့်ပေးပါ။")
    st.stop()

genai.configure(api_key=api_key)

try:
    supported_models = [
        m.name for m in genai.list_models() 
        if 'generateContent' in m.supported_generation_methods
    ]
    if any("gemini-1.5-flash" in m for m in supported_models):
        target_model = [m for m in supported_models if "gemini-1.5-flash" in m][0]
    elif supported_models:
        target_model = supported_models[0]
    else:
        target_model = "models/gemini-1.5-flash"
    
    model = genai.GenerativeModel(target_model)
except Exception:
    model = genai.GenerativeModel("gemini-1.5-flash")

user_input = st.text_area("ဇာတ်လမ်း အကြောင်းအရာ ရိုက်ထည့်ပါ-", placeholder="ဒီနေရာမှာ ဇာတ်လမ်းအကျဉ်းကို ရိုက်ထည့်ပါ...")

if st.button("Generate Recap", type="primary"):
    if not user_input.strip():
        st.warning("ကျေးဇူးပြု၍ စာသား အရင် ရိုက်ထည့်ပေးပါ။")
    else:
        with st.spinner("AI က Movie Recap ရေးသားနေပါသည်..."):
            try:
                prompt = f"""
                သင်သည် ကျွမ်းကျင်သော Burmese Movie Recapper တစ်ဦး ဖြစ်သည်။
                အောက်ပါ ဇာတ်လမ်းအချက်အလက်ကို အခြေခံပြီး မြန်မာဘာသာဖြင့် စိတ်ဝင်စားဖွယ် Movie Recap တစ်ခု ရေးပေးပါ:

                {user_input}
                """
                response = model.generate_content(prompt)
                st.success("အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ!")
                st.markdown("### ရလဒ်:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
