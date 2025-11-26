# دليل نشر المشروع على Streamlit Cloud

## ✅ الخطوات المكتملة

- [x] رفع المشروع على GitHub
- [x] الربط مع Streamlit Cloud
- [ ] إضافة Google Sheets Credentials كـ Secrets

---

## 🔐 إضافة Credentials إلى Streamlit Secrets

### الخطوة 1: افتح ملف credentials.json محلياً

انسخ **كل** محتويات ملف `credentials.json` (الملف الكامل)

### الخطوة 2: اذهب إلى Streamlit Cloud

1. اذهب إلى: https://share.streamlit.io
2. افتح تطبيقك
3. اضغط على **⚙️ Settings** (أعلى اليمين)
4. اختر **Secrets** من القائمة الجانبية

### الخطوة 3: أضف Secrets بهذا الشكل

في صندوق Secrets، الصق هذا النص ثم عدّل القيم:

```toml
# Google Cloud Platform Service Account
[gcp_service_account]
type = "service_account"
project_id = "ضع project_id من ملف credentials.json"
private_key_id = "ضع private_key_id من ملف credentials.json"
private_key = "ضع private_key الكامل من ملف credentials.json (مع \\n)"
client_email = "ضع client_email من ملف credentials.json"
client_id = "ضع client_id من ملف credentials.json"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "ضع client_x509_cert_url من ملف credentials.json"
```

### ⚠️ ملاحظة مهمة للـ private_key

عند نسخ `private_key`، تأكد من:
- النسخ الكامل بما في ذلك `-----BEGIN PRIVATE KEY-----` و `-----END PRIVATE KEY-----`
- إبقاء `\\n` كما هي (لا تستبدلها بأسطر جديدة)

**مثال:**
```toml
private_key = "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqh...باقي المفتاح...\\n-----END PRIVATE KEY-----\\n"
```

---

## 📋 نموذج كامل (استبدل القيم)

افتح `credentials.json` وانسخ القيم المقابلة:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-123456"
private_key_id = "abc123def456..."
private_key = "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\\n-----END PRIVATE KEY-----\\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

---

## 🎬 بعد إضافة Secrets

1. اضغط **Save**
2. الموقع سيعيد التشغيل تلقائياً
3. ✅ يجب أن يعمل الاتصال بـ Google Sheets الآن!

---

## 🔍 التحقق من الاتصال

بعد إضافة Secrets:
- افتح التطبيق
- اذهب إلى صفحة "المشرفون"
- إذا ظهرت البيانات أو رسالة ترحيبية → ✅ نجح الاتصال
- إذا ظهر خطأ JWT → راجع الخطوات أعلاه

---

## ⚠️ أمان: لا ترفع credentials.json على GitHub!

### تأكد من وجود .gitignore:

```gitignore
credentials.json
*.pyc
__pycache__/
.env
.streamlit/secrets.toml
```

### إذا رفعت credentials.json بالخطأ:

1. **احذفه من GitHub:**
   ```bash
   git rm --cached credentials.json
   git commit -m "Remove credentials.json"
   git push
   ```

2. **⚠️ CRITICAL:** أذهب إلى Google Cloud Console وأنشئ Service Account جديد!
   - المفاتيح المكشوفة غير آمنة ويجب تغييرها فوراً

---

## 📞 استكشاف الأخطاء

### خطأ: "Invalid JWT Signature"
**الحل:** تحقق من:
- نسخ `private_key` بالكامل مع `\\n`
- عدم وجود مسافات إضافية
- تطابق `client_email` و `project_id`

### خطأ: "Permission denied"
**الحل:** تأكد من:
- Share Google Sheet مع `client_email`
- Service Account له صلاحيات Editor

### خطأ: "Spreadsheet not found"
**الحل:**
- افتح Google Sheets يدوياً
- اذهب إلى Share
- أضف `client_email` من credentials.json
- اختر "Editor" permissions

---

## ✅ قائمة التحقق النهائية

- [ ] نسخت كل محتويات credentials.json
- [ ] أضفت Secrets في Streamlit Cloud بتنسيق TOML
- [ ] حفظت التغييرات
- [ ] Google Sheet مشارك مع Service Account Email
- [ ] أعدت تشغيل التطبيق
- [ ] اختبرت صفحة "المشرفون"
