import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Burmese Movie Recap Generator",
    page_icon=""
)

st.title("Burmese Movie Recap Generator")
st.write("ဇာတ်လမ်း အကျဉ်း သို့မဟုတ် အကြောင်းအရာကို ထည့်သွင်းပေးပါ။")

# Gemini API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key မတွေ့ပါ။ Settings တွင် GEMINI_API_KEY ထည့်ပေးပါ။")
    st.stop()

genai.configure(api_key=api_key)

# Gemini Model
try:
    supported_models = [
        m.name
        for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]

    # Gemini 3.6 Flash ကို အရင်ရှာမယ်
    gemini_36_models = [
        m for m in supported_models
        if "gemini-3.6-flash" in m
    ]

    if gemini_36_models:
        target_model = gemini_36_models[0]
    elif supported_models:
        target_model = supported_models[0]
    else:
        target_model = "models/gemini-3.6-flash"

    model = genai.GenerativeModel(target_model)

except Exception:
    model = genai.GenerativeModel("gemini-3.6-flash")


# User Input
user_input = st.text_area(
    "ဇာတ်လမ်း အကြောင်းအရာ ရိုက်ထည့်ပါ-",
    placeholder="ဒီနေရာမှာ ဇာတ်လမ်းအကျဉ်းကို ရိုက်ထည့်ပါ..."
)


# Generate Button
if st.button("Generate Recap", type="primary"):

    if not user_input.strip():
        st.warning("ကျေးဇူးပြု၍ စာသား အရင် ရိုက်ထည့်ပေးပါ။")

    else:
        with st.spinner("AI က Movie Recap ရေးသားနေပါသည်..."):

            try:
                prompt = f"""
သင်သည် ကျွမ်းကျင်သော Burmese Movie Recapper တစ်ဦး ဖြစ်သည်။

အောက်ပါ ဇာတ်လမ်းအချက်အလက်ကို အခြေခံပြီး
မြန်မာဘာသာဖြင့် စိတ်ဝင်စားဖွယ် Movie Recap တစ်ခု ရေးပေးပါ။

လိုအပ်ချက်များ:
- မြန်မာဘာသာဖြင့် ရေးပါ။
- ဇာတ်လမ်းကို နားလည်လွယ်အောင် ရေးပါ။
- အရေးကြီးသော ဇာတ်ကောင်များနှင့် ဖြစ်ရပ်များကို မလွတ်စေနဲ့။
- စာဖတ်သူ စိတ်ဝင်စားအောင် ဆက်တိုက်ရေးပါ။
- မလိုအပ်သော အချက်အလက်များ မထည့်ပါနှင့်။

ဇာတ်လမ်းအကြောင်းအရာ:
{user_input}
"""

                response = model.generate_content(prompt)

                result = response.text

                st.success("အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ!")

                st.markdown("### ရလဒ်:")

                st.text_area(
                    "Movie Recap",
                    value=result,
                    height=500
                )

                st.caption("အပေါ်က စာသားအကွက်ထဲကနေ Recap ကို ဖိထားပြီး Copy လုပ်နိုင်ပါတယ်။")

            except Exception as e:
                st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
