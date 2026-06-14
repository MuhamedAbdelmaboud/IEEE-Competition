import streamlit as st
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression

# المدن دي جبتها من Google Maps بنفسي
# الاتنين ارقام دول اسمهم latitude و longitude وبيحددوا المكان على الخريطة
cities = {
    "القاهرة": {"lat": 30.0626, "lon": 31.2497},
    "الإسكندرية": {"lat": 31.2001, "lon": 29.9187},
    "الجيزة": {"lat": 30.0131, "lon": 31.2089},
    "أسوان": {"lat": 24.0889, "lon": 32.8998},
    "الأقصر": {"lat": 25.6872, "lon": 32.6396},
    "بورسعيد": {"lat": 31.2653, "lon": 32.3019},
    "السويس": {"lat": 29.9668, "lon": 32.5498},
    "المنصورة": {"lat": 31.0364, "lon": 31.3807},
    "طنطا": {"lat": 30.7865, "lon": 31.0004},
    "الزقازيق": {"lat": 30.5877, "lon": 31.5021},
}

# الفانكشن دي بتجيب درجة الحرارة من الانترنت
# بتبعت request لموقع open-meteo وده موقع مجاني بيديك الطقس
def get_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # الداتا بترجع json وانا بستخرج منها درجة الحرارة بالسيلسيوس
        temp_c = data["current_weather"]["temperature"]
        
        # الداتا بتاعتنا بالفهرنهايت فلازم احول
        # المعادلة دي معادلة التحويل العادية
        temp_f = (temp_c * 9/5) + 32
        
        return temp_c, round(temp_f, 1)
    
    except:
        # لو في اي مشكلة في الانترنت ارجع None
        return None, None


# الفانكشن دي بتدرب الموديل على الداتا
def train_model():
    # قراءة الداتا من الملف
    df = pd.read_csv("Ice_Cream_Sales_-_temperatures.csv")
    
    # X هي الـ input يعني درجة الحرارة
    X = df[["Temperature"]].values
    
    # y هي الـ output يعني سعر الايس كريم
    y = df["Ice Cream Profits"].values
    
    # بعمل الموديل وبدربه على الداتا
    model = LinearRegression()
    model.fit(X, y)
    
    return model


# ===== الواجهة بتاعت streamlit =====

st.title("متوقع سعر الآيس كريم")
st.write("اختار مدينتك وهنقولك الآيس كريم بكام النهارده!")

# بدرب الموديل اول ما الابلكيشن يشتغل
model = train_model()

# القايمة دي بتخلي اليوزر يختار مدينته
city = st.selectbox("اختار مدينتك", list(cities.keys()))

# لما اليوزر يضغط الزرار
if st.button("احسب السعر"):
    
    # بجيب الـ lat و lon بتاعت المدينة اللي اختارها
    lat = cities[city]["lat"]
    lon = cities[city]["lon"]
    
    # بجيب درجة الحرارة من الانترنت
    temp_c, temp_f = get_temperature(lat, lon)
    
    # لو مجبتش درجة الحرارة يطلع error
    if temp_f is None:
        st.error("مش قادر يجيب درجة الحرارة دلوقتي، حاول تاني!")
    
    else:
        # بدي درجة الحرارة للموديل عشان يتنبأ بالسعر
        predicted_price = model.predict([[temp_f]])[0]
        
        # بعمل round للرقم عشان ميبقاش فيه ارقام كتير بعد الفاصلة
        predicted_price = round(predicted_price, 2)
        
        # بعرض النتايج للمستخدم
        st.success(f"درجة الحرارة في {city} دلوقتي: {temp_c}°C")
        st.metric(label="السعر المتوقع للآيس كريم", value=f"${predicted_price}")