import streamlit as st
import google.generativeai as genai

# စာမျက်နှာ ဒီဇိုင်း
st.set_page_config(page_title="Burmese Movie Recap", page_icon="", layout="centered")

st.title(" Burmese Movie Recap Generator")
st.write("ဇာတ်လမ်း အကျဉ်း သို့မဟုတ် အကြောင်းအရာကို ထည့်သွင်းပေးပါ။")

# Secret ထဲမှ API Key ကို ရယူခြင်း
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key မတွေ့ပါ။ Settings တွင် GEMINI_API_KEY ထည့်သွင်းပေးပါ။")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModelgemini-pro (သို့မဟုတ် models/gemini-1.5-flash-latest) သို့ ပြောင်းပေးပါ-

    # User စာရိုက်ထည့်ရမည့် နေရာ
    user_input = st.text_area("ဇာတ်လမ်း အကြောင်းအရာ ရိုက်ထည့်ပါ-", height=180, placeholder="ဒီနေရာမှာ ဇာတ်လမ်းအကျဉ်းကို ရိုက်ထည့်ပါ...")

    if st.button("Generate Recap ", type="primary"):
        if not user_input.strip():
            st.warning("ကျေးဇူးပြု၍ စာသား အရင် ရိုက်ထည့်ပေးပါ။")
        else:
            with st.spinner("AI က Movie Recap ရေးသားနေပါသည်..."):
                try:
                    prompt = f"""
                    သင်သည် ကျွမ်းကျင်သော Burmese Movie Recapper တစ်ဦး ဖြစ်သည်။ 
                    အောက်ပါ ဇာတ်လမ်းအချက်အလက်များကို အခြေခံ၍ လူစိတ်ဝင်စားဖွယ်၊ စကားပြောဟန် ရသမြောက်သော Burmese Movie Recap တစ်ခုအဖြစ် ဖန်တီးရေးသားပေးပါ:
                    
                    {user_input}
                    """
                    response = model.generate_content(prompt)
                    st.success("အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ!")
                    st.markdown("###  ရလဒ်:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
