import streamlit as st
import pandas as pd
import requests

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
def get_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        temp_c = data["current_weather"]["temperature"]
        # تحويل من سيلسيوس لفهرنهايت لان الداتا بتاعتنا بالفهرنهايت
        temp_f = (temp_c * 9/5) + 32
        return temp_c, round(temp_f, 1)
    except:
        return None, None

# الفانكشن دي بتحسب الـ slope و intercept بتاع الـ linear regression بدون مكتبات
# المعادلة دي اسمها least squares وبتلاقي افضل خط يمشي على الداتا
def train_model(df):
    X = df["Temperature"].values
    y = df["Ice Cream Profits"].values

    n = len(X)
    mean_x = sum(X) / n
    mean_y = sum(y) / n

    # بحسب الـ slope يعني ميل الخط
    numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((X[i] - mean_x) ** 2 for i in range(n))
    slope = numerator / denominator

    # بحسب الـ intercept يعني نقطة بداية الخط
    intercept = mean_y - slope * mean_x

    return slope, intercept

# الواجهة بتاعت streamlit

st.title("متوقع سعر الآيس كريم")
st.write("اختار محافظتك وهنقولك الآيس كريم بكام النهارده")

# بقرا الداتا وبدرب الموديل
df = pd.read_csv("Ice_Cream_Sales_temperatures.csv")
slope, intercept = train_model(df)

# سعر الصرف تقريبي
USD_TO_EGP = 50

# القايمة دي بتخلي اليوزر يختار مدينته
city = st.selectbox("اختار محافظتك", list(cities.keys()))

# لما اليوزر يضغط الزرار
if st.button("احسب السعر"):

    lat = cities[city]["lat"]
    lon = cities[city]["lon"]

    temp_c, temp_f = get_temperature(lat, lon)

    if temp_f is None:
        st.error("مش قادر يجيب درجة الحرارة دلوقتي، حاول تاني")
    else:
        # معادلة الخط: y = slope * x + intercept
        predicted_price_usd = slope * temp_f + intercept

        # بحول السعر من دولار لجنيه
        predicted_price_egp = round(predicted_price_usd * USD_TO_EGP, 2)

        st.success(f"درجة الحرارة في {city} دلوقتي: {temp_c}°C")
        st.metric(label="السعر المتوقع للآيس كريم", value=f"EGP {predicted_price_egp}")
        st.caption("السعر تقريبي بناءً على درجة الحرارة")
