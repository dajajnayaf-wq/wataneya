# AGENTS.md

متجر «دواجن الوطنية» — موقع عربي RTL لتوصيل منتجات طازجة في السعودية.

> ملاحظة: الاسم التجاري الحالي **دواجن الوطنية** (شعار نصّي `و` + الاسم، اللون `#2d6a4f`).
> بقايا مشاريع سابقة ما زالت في المستودع بأسماء «مزرعتي» / «كبش نجد» / «أرياف» — تجاهلها،
> والصفحات الفعّالة هي المذكورة أدناه. العملة: الريال السعودي `ر.س`، والسعر بثلاث خانات عشرية.

## البنية

- **الكتالوج** في Firestore (مشروع `kuwait-me`، مجموعة `products`) — المصدر الموثّق الوحيد.
  حقول الوثيقة: `name`, `desc`, `price` (نص بثلاث خانات عشرية مثل `"26.500"`), `img`, `order` (رقم).
- **الصفحات**: `index.html` هي صفحة عرض واحد (Landing) للمنتج المميز، وتعريفه في
  `staticProduct` أسفل الملف — حرّره مباشرةً. أما `creatprogect.html` (لوحة الإدارة) فيحمل
  نسخة مدمجة `defaultProducts` للعرض الفوري ثم تُزامَن من Firestore؛ لا تحرّر كتلة
  `defaultProducts` يدوياً — شغّل `python3 tools/sync_default_products.py`.
- **العرض الحالي**: بوكس 10 حبات دجاج (900 غ لكل حبة) + 5 صحون صدور (500 غ لكل صحن) +
  كيس أرز بسمتي 10 كيلو، بسعر 30.000 ر.س، بصورته `assets/images/product-offer.png`.
- **الصور**: محلية في `assets/images/products/*.webp`، والمسارات في `img` تبدأ بـ `/`.
- **الشعار**: `assets/images/alwatania-logo.png` (للخلفيات الفاتحة) و`alwatania-logo-white.png`
  (للدخلفيات الداكنة)، وكلاهما يُشتقّ من ملف الشعار المصدر بـ `python3 tools/prepare_logo.py`.
  تغيير الشعار في مكان واحد: استبدل `assets/images/alwatania-logo-white.png` ثم أعد تشغيل السكربت.
- **صورة العرض**: `assets/images/product-offer.png` مولّدة بـ `python3 tools/make_product_image.py`
  (عدّل قيم `OFFER` في السكربت لإعادة توليدها). كل الصفحات تشير إلى هذا المسار الواحد.
- **السلة** (`assets/js/cart.js`): تعرّف المنتج **بالاسم فقط** (`p.name === name`).
  لذلك يجب أن تكون أسماء المنتجات فريدة، وإلا اندمج منتجان في سطر واحد بأسعار مختلطة.
- **صفحة المنتج**: `/product/<id>/<slug>` تُخدم كلها بصفحة واحدة `product/index.html`
  (ديناميكية — تقرأ المعرّف من المسار وتجلب من Firestore). لا تنشئ صفحات ثابتة لكل منتج،
  فهي تصبح قديمة بعد أي تعديل. أعد البناء بـ `python3 tools/build_product_page.py`.

## الأوامر

```bash
python3 tools/sync_default_products.py    # مزامنة defaultProducts في index.html و creatprogect.html
python3 tools/build_product_page.py       # إعادة بناء product/index.html
python3 tools/preview_server.py 12000     # معاينة تحاكي توجيهات Netlify (لأن http.server يرجّع 404)
```

## أدوات Firestore (`tools/`)

`add_products_to_firestore.py` يوفر `BASE`, `panel_credentials`, `sign_in`, `get/patch/post`,
`firestore_get`, `update_doc` (يحوّل `int` → `integerValue` و `str` → `stringValue`).
استخدم `update_doc(doc_id, {...}, token)` لتعديل حقول محددة دون مسح الباقي.

سكربتات الإدخال الجماعي (`arabize_chicken.py`, `dedupe_product_names.py`) تعتمد على
`firestore-import-result.json` لربط صفوف المصدر بمعرّفات الوثائق.

## التوجيه (Netlify)

`netlify.toml`: `/product/*` → `/product/index.html`، ثم كل ما تبقى → `/index.html`.
Netlify يخدم الملفات الحقيقية قبل تطبيق الـ redirects.

## تحذير أمني مفتوح

`assets/js/firebase-client.js` يحتوي على `PANEL_EMAIL` و`PANEL_PASSWORD` مكتوبين صريح
(حساب الإدارة). أي زائر يستطيع قراءتهما من المتصفح ويملك صلاحية الكتابة على `products`.
يجب نقل الكتابة إلى خادم/Cloud Function مع قواعد أمان تمنع الكتابة المجهولة.
