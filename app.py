import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SME Response Architect", page_icon="🇰🇿")

st.title("🇰🇿 SME Sentiment & Response Architect")
st.subheader("AI Tool for Almaty SMEs" \
"")

api_key = st.sidebar.text_input("Введите Gemini API Key", type="password")
user_input = st.text_area("Вставьте текст отзыва клиента:", height=150)

if st.button("Проанализировать"):
    if not api_key:
        st.error("Введите API ключ в боковой панели!")
    elif not user_input:
        st.warning("Введите текст отзыва.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Автоматический поиск доступной модели
            with st.spinner('Поиск доступной модели и анализ...'):
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not available_models:
                    st.error("Для вашего ключа не найдено доступных моделей.")
                else:
                    # Выбираем самую новую из доступных (обычно 1.5-flash или 1.0-pro)
                    selected_model = available_models[0]
                    model = genai.GenerativeModel(selected_model)
                    
                    prompt = f"""
                    Analyze this business review from Kazakhstan: "{user_input}"
                    Format:
                    1. Sentiment (Positive/Negative/Neutral)
                    2. Category (Food/Service/Atmosphere/Price)
                    3. Reply in Russian
                    4. Reply in Kazakh
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.success(f"Готово! (Использована модель: {selected_model})")
                    st.markdown(response.text)
                    
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
            st.info("Совет: Убедитесь, что в Google AI Studio вы создали 'API key in new project'.")