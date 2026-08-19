import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Burmese Movie Recap Generator",
    page_icon="🎬"
)

# =========================
# WEBSITE UI
# =========================

st.title("Burmese Movie Recap Generator")
st.write("ဇာတ်လမ်း အကျဉ်း သို့မဟုတ် အကြောင်းအရာကို ထည့်သွင်းပေးပါ။")

# =========================
# GEMINI API
# User မမြင်နိုင်တဲ့ Backend
# =========================

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("ဝန်ဆောင်မှုကို လက်ရှိအသုံးပြု၍ မရသေးပါ။")
    st.stop()

genai.configure(api_key=api_key)

try:
    supported_models = [
        m.name
        for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]

    # Gemini 3.6 Flash ရှိရင် အဲဒါကိုသုံးမယ်
    target_models = [
        m for m in supported_models
        if "gemini-3.6-flash" in m
    ]

    if target_models:
        target_model = target_models[0]
    elif supported_models:
        target_model = supported_models[0]
    else:
        target_model = "models/gemini-3.6-flash"

    model = genai.GenerativeModel(target_model)

except Exception:
    # Backend မှာပဲ Error ဖြစ်မယ်
    model = None


# =========================
# USER INPUT
# =========================

user_input = st.text_area(
    "ဇာတ်လမ်း အကြောင်းအရာ ရိုက်ထည့်ပါ-",
    placeholder="ဒီနေရာမှာ ဇာတ်လမ်းအကျဉ်းကို ရိုက်ထည့်ပါ..."
)


# =========================
# GENERATE
# =========================

if st.button("Generate Recap", type="primary"):

    if not user_input.strip():
        st.warning("ကျေးဇူးပြု၍ ဇာတ်လမ်းအကြောင်းအရာ အရင်ထည့်ပေးပါ။")

    elif model is None:
        # User ကို Gemini/API/Python error မပြ
        st.error("ဝန်ဆောင်မှုတွင် ခေတ္တအခက်အခဲ ဖြစ်နေပါသည်။ ခဏအကြာတွင် ပြန်လည်ကြိုးစားပေးပါ။")

    else:
        with st.spinner("AI က Movie Recap ရေးသားနေပါသည်..."):

            try:
                prompt = f"""
သင်သည် ကျွမ်းကျင်သော Burmese Movie Recapper တစ်ဦး ဖြစ်သည်။

အောက်ပါ ဇာတ်လမ်းအချက်အလက်ကို အခြေခံပြီး
မြန်မာဘာသာဖြင့် စိတ်ဝင်စားဖွယ် Movie Recap တစ်ခု ရေးပေးပါ။

လိုအပ်ချက်များ:
- မြန်မာဘာသာဖြင့် ရေးပါ။
- နားလည်လွယ်အောင် ရေးပါ။
- အရေးကြီးသော ဇာတ်ကောင်များနှင့် ဖြစ်ရပ်များကို မလွတ်စေနဲ့။
- ဇာတ်လမ်းကို အစမှအဆုံး ဆက်စပ်ပြီး ရေးပါ။
- စိတ်ဝင်စားဖွယ် Movie Recap ပုံစံဖြင့် ရေးပါ။
- မလိုအပ်သော အချက်အလက်များ မထည့်ပါနှင့်။

ဇာတ်လမ်းအကြောင်းအရာ:
{user_input}
"""

                response = model.generate_content(prompt)

                result = response.text

                st.success("အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ!")

                st.markdown("### ရလဒ်:")

                # User က လွယ်လွယ် Copy လုပ်နိုင်အောင်
                st.text_area(
                    "Movie Recap",
                    value=result,
                    height=500
                )

            except Exception:
                # ❗ Gemini error / API error / Model error
                # User ဘက်မှာ အသေးစိတ်မပြ
                st.error(
                    "ဝန်ဆောင်မှုတွင် ခေတ္တအခက်အခဲ ဖြစ်နေပါသည်။ "
                    "ခဏအကြာတွင် ပြန်လည်ကြိုးစားပေးပါ။"
                )
