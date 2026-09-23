"""
Yasal sayfaların içeriği: Gizlilik Politikası, KVKK Aydınlatma Metni, Açık Rıza Metni, Kullanım Koşulları.

ÖNEMLİ — yayından önce (şahıs şirketi kurulduktan sonra):
  1. TRADE_NAME, TAX_OFFICE, TAX_NO ve ADDRESS alanlarını vergi levhasındaki bilgilerle doldurun.
  2. İletişim e-postasının (CONTACT_EMAIL) gerçekten çalıştığını doğrulayın.
  3. Metinleri bir avukata okutun (hukukçu dosyasındaki sorularla birlikte).
Metinler uygulamanın kodda gerçekten yaptığına göre yazılmıştır; özellik değiştikçe güncellenmelidir.
"""

# Veri sorumlusu: şahıs işletmesi (gerçek kişi tacir). Unvanda işletme sahibinin adı soyadı zorunludur.
OWNER = "Hasibe Akca"
TRADE_NAME = "[TİCARİ UNVAN — ör. Hasibe Akca – HMFA Yazılım ve Bilişim Hizmetleri]"
TAX_OFFICE = "[VERGİ DAİRESİ]"
TAX_NO = "[VERGİ NO]"
ADDRESS = "[İŞ YERİ ADRESİ]"
CONTROLLER = TRADE_NAME
CONTACT_EMAIL = "destek@dozunda.com"
VERSION = "Sürüm 1.0"
EFFECTIVE = "[YÜRÜRLÜK TARİHİ]"


def _h2(t):
    return f"<h2>{t}</h2>"


def _p(t):
    return f"<p>{t}</p>"


def _ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


META = f"{VERSION} · Yürürlük: {EFFECTIVE}"

# ------------------------------------------------------------------ ortak bölümler
CONTROLLER_BLOCK = _p(
    f"<b>Veri sorumlusu:</b> {TRADE_NAME}<br>"
    f"<b>İşletme sahibi:</b> {OWNER}<br>"
    f"<b>Vergi dairesi / no:</b> {TAX_OFFICE} / {TAX_NO}<br>"
    f"<b>Adres:</b> {ADDRESS}<br>"
    f'<b>E-posta:</b> <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
)

DATA_TABLE = _table(
    ["Veri kategorisi", "Örnekler", "Neden işlenir"],
    [
        ["Kimlik", "Ad, soyad, doğum tarihi, cinsiyet", "Hesabınızı oluşturmak, size hitap etmek, yaşa ve cinsiyete uygun bilgi göstermek"],
        ["İletişim", "Cep telefonu numarası (şifrelenmiş özet olarak), adres (girerseniz)", "Giriş ve doğrulama; acil durum ekranında adresinizi gösterebilmek"],
        ["Sağlık", "Kullandığınız ilaçlar, hatırlatıcılar ve doz kayıtları, alerjiler, kronik hastalıklar, ameliyatlar, kilo, gebelik ve emzirme durumu, regl döngüsü kayıtları, gebelik günlüğü notları ve ultrason görüntüleri, cilt ve saç analizi yanıtları", "İlaç etkileşim kontrolü, hatırlatma, kişisel sağlık takibi — yalnızca açık rızanızla"],
        ["Aile üyesi bilgileri", "Eklediğiniz aile üyelerinin adı, yakınlık derecesi, doğum tarihi ve sağlık bilgileri", "Aile üyeleriniz için hatırlatıcı ve etkileşim kontrolü"],
        ["Yakın takibi", "Eşleştiğiniz kişi, onay tarihi, gönderilen hatırlatmalar", "Onay verdiğiniz yakınınızın ilaç ve doz bilgisini görebilmesi"],
        ["Eczane talebi", "Talep ettiğiniz ilaç adları, reçete numarası veya görüntüsü, talep anındaki konumunuz, eczaneyle yazışmalar", "İlacınızı yakınınızdaki eczanelerden sorabilmeniz"],
        ["Konum", "Yalnızca eczane talebi ve yakın eczane araması sırasında anlık konum", "Size yakın eczaneleri bulmak"],
        ["Kullanım ve cihaz", "Misafir cihaz kimliği, arama ve etkileşim sorgusu kayıtları, IP adresi, cihaz ve tarayıcı bilgisi, bildirim kimliği", "Hizmetin güvenliği, hataların giderilmesi, bildirim gönderimi, anonim istatistik"],
        ["Talep ve iletişim", "Uzman görüşmesi gibi yakında açılacak özelliklere bıraktığınız talep; web sitesi başvuru formu (ad, e-posta, telefon, mesaj)", "Size geri dönmek, özellik açıldığında haber vermek"],
    ],
)

PROCESSORS = _table(
    ["Hizmet sağlayıcı", "Ne için", "Konum"],
    [
        ["Supabase", "Veritabanı ve dosya depolama (gebelik günlüğü görüntüleri dahil)", "Yurt dışı (bulut sunucu)"],
        ["Render", "Uygulama sunucusu ve web sitesi barındırma", "Yurt dışı (Avrupa Birliği — Frankfurt)"],
        ["OneSignal", "Bildirim (push) gönderimi", "Yurt dışı (ABD)"],
        ["Google (Play, Android)", "Uygulamanın dağıtımı ve bildirim altyapısı", "Yurt dışı"],
        ["CollectAPI", "Nöbetçi eczane listesi (kişisel veri gönderilmez; yalnızca il ve ilçe)", "Türkiye"],
    ],
)

RIGHTS = _ul([
    "Kişisel verilerinizin işlenip işlenmediğini öğrenme,",
    "İşlenmişse buna ilişkin bilgi talep etme,",
    "İşlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme,",
    "Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme,",
    "Eksik veya yanlış işlenmişse düzeltilmesini isteme,",
    "KVKK'nın 7. maddesindeki şartlar çerçevesinde silinmesini veya yok edilmesini isteme,",
    "Düzeltme, silme ve yok etme işlemlerinin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme,",
    "Münhasıran otomatik sistemlerle analiz edilmesi sonucu aleyhinize bir sonuç çıkmasına itiraz etme,",
    "Kanuna aykırı işleme sebebiyle zarara uğramanız halinde zararın giderilmesini talep etme.",
])

DELETE_BLOCK = "".join([
    _p("Hesabınızı ve verilerinizi iki yoldan silebilirsiniz:"),
    _ul([
        "<b>Uygulamadan:</b> Profil › Ayarlar › Hesabımı Sil. Hesabınız hemen devre dışı kalır; 90 gün içinde tekrar giriş yaparak geri açabilirsiniz. 90 günün sonunda hesabınız ve ona bağlı tüm veriler (sağlık kayıtları, hatırlatıcılar, doz kayıtları, yakın bağlantıları, gebelik günlüğü görüntüleri dahil) kalıcı olarak silinir.",
        f'<b>E-postayla:</b> Uygulamaya erişemiyorsanız kayıtlı telefon numaranızı belirterek <a href="mailto:{CONTACT_EMAIL}?subject=Hesap%20silme%20talebi">{CONTACT_EMAIL}</a> adresine "Hesap silme talebi" konulu bir e-posta gönderin. Kimliğinizi doğruladıktan sonra talebinizi en geç 30 gün içinde sonuçlandırırız.',
    ]),
    _p("Tek tek kayıtları (bir hatırlatıcıyı, aile üyesini, gebelik günlüğü kaydını, yakın bağlantısını) istediğiniz zaman uygulama içinden silebilirsiniz."),
])

# ------------------------------------------------------------------ Gizlilik Politikası
PRIVACY = "".join([
    _p("Bu politika, Dozunda mobil uygulamasını ve web sitesini kullanırken hangi bilgilerinizi topladığımızı, "
       "bunları nasıl kullandığımızı ve koruduğumuzu sade bir dille anlatır. Kişisel verilerinizin işlenmesine ilişkin "
       'yasal bilgilendirme için <a href="/kvkk/">KVKK Aydınlatma Metni</a>\'ni de okuyabilirsiniz.'),
    _h2("1. Kim sorumlu?"),
    CONTROLLER_BLOCK,
    _h2("2. Hangi bilgileri topluyoruz?"),
    _p("Üye olmadan kullandığınız özelliklerde (ilaç etkileşim kontrolü, nöbetçi eczane) sizi tanımlayan bir bilgi "
       "istemeyiz; yalnızca cihazınıza atanan rastgele bir misafir kimliği ve hizmetin çalışması için gereken teknik "
       "kayıtlar tutulur. Üye olduğunuzda ve özellikleri kullandıkça aşağıdaki bilgiler işlenir:"),
    DATA_TABLE,
    _p("T.C. kimlik numaranızı istemiyoruz. Uygulamanın eski bir sürümüyle kayıt olduysanız, o sürümde alınan kimlik "
       "numaranız yalnızca geri döndürülemez şekilde şifrelenmiş bir özet olarak durur ve artık hiçbir işlemde kullanılmaz."),
    _h2("3. Bilgilerinizi nasıl kullanıyoruz?"),
    _ul([
        "Hesabınızı oluşturmak ve güvenli girişinizi sağlamak,",
        "İlaçlarınızın birbiriyle etkileşimini kontrol etmek,",
        "İlaç saatinizde hatırlatma göndermek ve doz geçmişinizi tutmak,",
        "Onay verdiğiniz yakınınızın ilaç ve doz bilgilerinizi görebilmesini sağlamak,",
        "Nöbetçi ve yakın eczaneleri bulmak, eczane taleplerinizi iletmek,",
        "Hizmetin güvenliğini sağlamak, hataları gidermek ve hizmeti geliştirmek (kimliksizleştirilmiş, toplu istatistiklerle).",
    ]),
    _p("<b>Sağlık verilerinizi satmıyoruz, reklam amacıyla kullanmıyor ve reklam platformlarıyla paylaşmıyoruz.</b> "
       "Sağlık verileriniz yalnızca açık rızanızla işlenir."),
    _h2("4. Bilgilerinizi kimler görebilir?"),
    _ul([
        "<b>Siz:</b> Tüm kayıtlarınızı görür, düzenler ve silersiniz.",
        "<b>Onay verdiğiniz yakınınız:</b> Yakın takibinde yalnızca hatırlatıcılarınızı ve dozlarınızı aldığınız bilgisini görür. Alerji, hastalık, regl, gebelik günlüğü gibi diğer bilgileriniz paylaşılmaz. Onayınızı istediğiniz an geri alabilirsiniz.",
        "<b>Eczaneler:</b> Bir ilaç talebi oluşturduğunuzda talebiniz (ilaç adları, varsa reçete numarası veya görüntüsü) konumunuzun yakınındaki (yaklaşık 10 km) eczanelere iletilir. Eczaneyle yazışmalarınızı ilgili eczane görür.",
        "<b>Hizmet sağlayıcılarımız:</b> Aşağıdaki altyapı hizmetleri, verilerinizi yalnızca bizim adımıza ve hizmetin çalışması için işler.",
        "<b>Yetkili kamu kurumları:</b> Yalnızca yasal bir zorunluluk olduğunda.",
    ]),
    PROCESSORS,
    _p("Bu hizmet sağlayıcıların bir kısmının sunucuları yurt dışındadır; kişisel verilerinizin yurt dışına "
       "aktarılması KVKK'nın 9. maddesine uygun şekilde yapılır."),
    _h2("5. Verilerinizi nasıl koruyoruz?"),
    _ul([
        "Uygulama ile sunucular arasındaki tüm iletişim şifreli bağlantı (HTTPS/TLS) üzerinden yapılır.",
        "Telefon numaranız düz metin olarak değil, geri döndürülemez şifrelenmiş bir özet olarak saklanır.",
        "Gebelik günlüğü görüntüleri herkese kapalı bir depolama alanında tutulur ve yalnızca sizin için üretilen, kısa süre (1 saat) geçerli bağlantılarla görüntülenir.",
        "Yakın eşleştirme kodları düz metin olarak saklanmaz; tek kullanımlıktır ve 10 dakika geçerlidir.",
        "Verilerinize erişim, her kaydın yalnızca sahibine (ve onay verdiği yakınına, kapsamı dahilinde) açık olacak şekilde sınırlandırılmıştır.",
    ]),
    _p("Hiçbir sistem tamamen risksiz değildir; bir veri güvenliği ihlali olursa KVKK uyarınca sizi ve Kişisel "
       "Verileri Koruma Kurulu'nu bilgilendiririz."),
    _h2("6. Uygulama izinleri"),
    _ul([
        "<b>Bildirimler:</b> İlaç saati, yakınınızdan gelen hatırlatma ve takip istekleri için. Kapatabilirsiniz; bu durumda hatırlatma alamazsınız.",
        "<b>Kamera:</b> İlaç kutusundaki karekodu okutmak ve isterseniz ultrason görüntüsünün fotoğrafını çekmek için.",
        "<b>Fotoğraflar:</b> Yalnızca sizin seçtiğiniz görüntüye (ör. ultrason, reçete) erişilir.",
        "<b>Konum:</b> Yalnızca eczane talebi ve yakın eczane araması sırasında; arka planda konumunuz izlenmez.",
    ]),
    _h2("7. Ne kadar süre saklıyoruz?"),
    _p("Verilerinizi hesabınız açık olduğu sürece saklarız. Hesabınızı sildiğinizde 90 günlük geri alma süresinin "
       "sonunda tüm verileriniz kalıcı olarak silinir. Yasal olarak saklamakla yükümlü olduğumuz kayıtlar varsa, "
       "yalnızca bu süre boyunca ve erişimi kısıtlanmış olarak tutulur."),
    _h2('<span id="hesap-silme">8. Hesabınızı ve verilerinizi silme</span>'),
    DELETE_BLOCK,
    _h2("9. Çocuklar"),
    _p("Dozunda'a üye olmak için 18 yaşını doldurmuş olmanız gerekir. 18 yaşından küçük çocuklarınız için uygulama "
       "içinde aile üyesi profili oluşturarak ilaçlarını kendi hesabınızdan yönetebilirsiniz; bu durumda çocuğunuzun "
       "bilgilerini veli sıfatıyla sizin girdiğiniz kabul edilir."),
    _h2("10. Web sitesi"),
    _p("Web sitemizde çerez kullanan reklam veya analiz aracı bulunmamaktadır. Başvuru formunu doldurursanız "
       "gönderdiğiniz bilgiler yalnızca size geri dönmek için kullanılır."),
    _h2("11. Haklarınız"),
    _p('KVKK kapsamındaki haklarınız ve başvuru yöntemi <a href="/kvkk/">KVKK Aydınlatma Metni</a>\'nde açıklanmıştır.'),
    _h2("12. Değişiklikler"),
    _p("Bu politikayı güncellediğimizde yeni sürümü bu sayfada yayımlar, önemli değişiklikleri uygulama içinden "
       "bildiririz."),
    _h2("13. İletişim"),
    CONTROLLER_BLOCK,
])

# ------------------------------------------------------------------ KVKK Aydınlatma Metni
KVKK = "".join([
    _p("Bu aydınlatma metni, 6698 sayılı Kişisel Verilerin Korunması Kanunu'nun (KVKK) 10. maddesi uyarınca, Dozunda "
       "mobil uygulaması ve web sitesi kapsamında kişisel verilerinizin işlenmesine ilişkin sizi bilgilendirmek "
       "amacıyla hazırlanmıştır."),
    _h2("1. Veri sorumlusu"),
    CONTROLLER_BLOCK,
    _h2("2. İşlenen kişisel veriler ve işleme amaçları"),
    DATA_TABLE,
    _h2("3. Hukuki sebepler"),
    _ul([
        "<b>Sözleşmenin kurulması ve ifası (KVKK md. 5/2-c):</b> Üyelik ve temel hizmetlerin sunulması için gereken kimlik, iletişim ve kullanım verileri.",
        "<b>Açık rıza (KVKK md. 6/2):</b> Özel nitelikli kişisel veri olan sağlık verileriniz. Açık rızanız olmadan sağlık verisi işlenmez.",
        "<b>Meşru menfaat (KVKK md. 5/2-f):</b> Hizmetin güvenliği, kötüye kullanımın önlenmesi ve hataların giderilmesi için tutulan teknik kayıtlar.",
        "<b>Hukuki yükümlülük (KVKK md. 5/2-ç):</b> Mevzuatın saklamayı veya yetkili makamlarla paylaşmayı zorunlu kıldığı durumlar.",
        "<b>Bir hakkın tesisi, kullanılması veya korunması (KVKK md. 5/2-e):</b> Olası uyuşmazlıklarda gereken kayıtlar.",
    ]),
    _h2("4. Toplama yöntemi"),
    _p("Kişisel verileriniz; mobil uygulama ve web sitesi üzerinden sizin girdiğiniz bilgiler, uygulamayı "
       "kullanımınız sırasında oluşan kayıtlar, izin verdiğiniz ölçüde cihazınızın kamera, fotoğraf ve konum "
       "özellikleri aracılığıyla elektronik ortamda, otomatik ve kısmen otomatik yollarla toplanır."),
    _h2("5. Aktarım"),
    _p("Kişisel verileriniz; onay vermeniz halinde yakın takibinde eşleştiğiniz kişiye (yalnızca ilaç ve doz "
       "bilgileri), eczane talebi oluşturmanız halinde yakınınızdaki eczanelere (talep kapsamındaki bilgiler), "
       "hizmetin sunulması için altyapı hizmeti aldığımız tedarikçilere ve yasal zorunluluk halinde yetkili kamu "
       "kurum ve kuruluşlarına aktarılabilir."),
    PROCESSORS,
    _p("Yurt dışında bulunan hizmet sağlayıcılara aktarım, KVKK'nın 9. maddesinde öngörülen şartlara ve "
       "güvencelere uygun olarak gerçekleştirilir."),
    _h2("6. Saklama süresi"),
    _p("Verileriniz hesabınız açık olduğu sürece saklanır. Hesabınızı sildiğinizde 90 günlük geri alma süresinin "
       "sonunda kalıcı olarak silinir; mevzuat gereği saklanması zorunlu kayıtlar bu süre boyunca erişimi "
       "kısıtlanarak tutulur."),
    _h2("7. KVKK md. 11 kapsamındaki haklarınız"),
    RIGHTS,
    _h2("8. Başvuru yöntemi"),
    _p(f"Haklarınıza ilişkin taleplerinizi, kimliğinizi tespit edici bilgilerle birlikte yazılı olarak {ADDRESS} "
       f'adresine veya kayıtlı telefon numaranızı belirterek <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> '
       "adresine iletebilirsiniz. Başvurunuz, talebin niteliğine göre en geç 30 gün içinde ücretsiz olarak "
       "sonuçlandırılır. Başvurunuzun reddedilmesi, verilen cevabı yetersiz bulmanız veya süresinde cevap "
       "verilmemesi halinde Kişisel Verileri Koruma Kurulu'na şikâyette bulunabilirsiniz."),
])

# ------------------------------------------------------------------ Açık Rıza Metni
CONSENT = "".join([
    _p('Bu metni okumadan önce <a href="/kvkk/">KVKK Aydınlatma Metni</a>\'ni incelemenizi öneririz.'),
    _h2("Neye rıza veriyorsunuz?"),
    _p(f"Dozunda uygulamasına girdiğim ve uygulamayı kullanırken oluşan aşağıdaki sağlık verilerimin, Dozunda'yı "
       f"işleten {CONTROLLER} tarafından aşağıda belirtilen amaçlarla işlenmesine açık rıza veriyorum:"),
    _ul([
        "Kullandığım ilaçlar, ilaç hatırlatıcılarım ve doz kayıtlarım,",
        "Alerjilerim, kronik hastalıklarım, geçirdiğim ameliyatlar ve kilom,",
        "Gebelik ve emzirme durumum, gebelik günlüğü notlarım ve ultrason görüntülerim,",
        "Regl döngüsü kayıtlarım,",
        "Cilt ve saç analizi için verdiğim yanıtlar,",
        "Eczane talebi oluşturduğumda ilaç adları ve reçete bilgilerim,",
        "Uygulamaya eklediğim aile üyelerimin yukarıdaki kategorilerdeki bilgileri.",
    ]),
    _h2("Hangi amaçlarla?"),
    _ul([
        "İlaçlarımın birbiriyle etkileşiminin kontrol edilmesi,",
        "İlaç saatimde hatırlatma yapılması ve doz geçmişimin tutulması,",
        "Kişisel sağlık takibi araçlarının (regl, gebelik, gebelik günlüğü) çalışması,",
        "Onay verdiğim yakınımın ilaç ve doz bilgilerimi görebilmesi,",
        "Eczane talebimin yakınımdaki eczanelere iletilmesi.",
    ]),
    _h2("Aile üyelerinin bilgileri"),
    _p("Başka bir kişinin (ör. annemin, çocuğumun) sağlık bilgilerini girdiğimde, bu kişiden gerekli onayı "
       "aldığımı veya kanuni temsilcisi olduğumu beyan ederim."),
    _h2("Rızanızı geri alma"),
    _p(f"Bu rızayı vermek zorunda değilsiniz. Rıza vermezseniz sağlık verisi gerektiren özellikler (hatırlatıcı, "
       f"sağlık bilgileri, gebelik günlüğü gibi) kullanılamaz; üye olmadan çalışan özellikler kullanılmaya devam eder. "
       f"Rızanızı dilediğiniz zaman uygulamada Profil › Gizlilik ve rıza bölümünden veya "
       f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> adresine yazarak geri alabilirsiniz. Geri almanız, '
       "o tarihe kadar yapılan işlemleri etkilemez."),
])

# ------------------------------------------------------------------ Kullanım Koşulları
TERMS = "".join([
    _p("Bu koşullar, Dozunda mobil uygulamasını ve web sitesini (\"Dozunda\") kullanımınızı düzenler. Dozunda, "
       "aşağıda bilgileri yer alan şahıs işletmesi tarafından işletilir. Dozunda'yı kullanarak bu koşulları kabul "
       "etmiş olursunuz."),
    _h2("1. Taraflar"),
    CONTROLLER_BLOCK,
    _h2("2. Hizmet"),
    _p("Dozunda; ilaç etkileşim kontrolü, ilaç hatırlatıcı, yakın takibi, nöbetçi eczane araması, eczane talebi, "
       "regl ve gebelik takibi gibi araçlar sunan ücretsiz bir sağlık asistanı uygulamasıdır. Özellikler zaman içinde "
       "eklenebilir, değiştirilebilir veya kaldırılabilir."),
    _h2("3. Önemli sağlık uyarısı"),
    _ul([
        "<b>Dozunda bir teşhis veya tedavi aracı değildir;</b> hekim ve eczacı danışmanlığının yerine geçmez.",
        "İlaç etkileşim sonuçları bilgilendirme amaçlıdır. Bir etkileşim görmemeniz iki ilacın her durumda güvenli olduğu anlamına gelmez; bir etkileşim görmeniz de ilacınızı kendi başınıza bırakmanız gerektiği anlamına gelmez.",
        "Hatırlatmalar internet bağlantısı, cihaz ayarları ve bildirim izinleri gibi etkenlere bağlıdır; ilacınızı zamanında almanın sorumluluğu size aittir. Hayati önemdeki ilaçlarda yalnızca uygulamaya güvenmeyin.",
        "<b>Acil durumlarda 112'yi arayın.</b>",
    ]),
    _h2("4. Üyelik"),
    _ul([
        "Üye olmak için 18 yaşını doldurmuş olmanız gerekir.",
        "Kayıtta verdiğiniz bilgilerin doğru olması ve telefon numaranızın size ait olması gerekir.",
        "Hesabınızın ve telefonunuzun güvenliğinden siz sorumlusunuz; yetkisiz kullanım fark ederseniz bize bildirin.",
    ]),
    _h2("5. Aile üyeleri ve yakın takibi"),
    _ul([
        "Başka bir kişinin bilgilerini girdiğinizde o kişinin onayını aldığınızı veya kanuni temsilcisi olduğunuzu kabul edersiniz.",
        "Yakın takibi yalnızca takip edilen kişinin kendi hesabından verdiği onayla başlar ve iki taraftan biri tarafından her an sonlandırılabilir.",
        "Yakın takibini, kişinin rızası dışında izlemek veya baskı kurmak amacıyla kullanamazsınız.",
    ]),
    _h2("6. Eczane talepleri"),
    _p("Dozunda ilaç satmaz, ödeme almaz ve ilacın teslimine aracılık etmez. Eczane talebi, ilacınızın yakınınızdaki "
       "eczanelerde bulunup bulunmadığını sormanızı sağlar. İlacın temini, satışı, fiyatı ve reçete kontrolü tamamen "
       "ilgili eczanenin sorumluluğundadır."),
    _h2("7. Kullanım kuralları"),
    _p("Dozunda'yı hukuka aykırı amaçlarla kullanamaz; başkalarının hesabına erişmeye, sistemi bozmaya, otomatik "
       "araçlarla veri toplamaya veya eczanelere ve diğer kullanıcılara yanıltıcı, rahatsız edici içerik göndermeye "
       "çalışamazsınız. Bu kurallara aykırı kullanımda hesabınız askıya alınabilir veya kapatılabilir."),
    _h2("8. Fikri haklar"),
    _p("Dozunda'nın yazılımı, tasarımı, markası ve içerikleri üzerindeki haklar saklıdır. Kendi girdiğiniz içeriklerin "
       "(notlar, görüntüler) hakları size aittir; bunları yalnızca size hizmet sunmak için işleriz."),
    _h2("9. Sorumluluk"),
    _p("Dozunda'yı kesintisiz ve hatasız sunmak için özen gösteririz; ancak bakım, altyapı sağlayıcılarından kaynaklanan "
       "kesintiler veya öngörülemeyen teknik sorunlar yaşanabilir. Kanunen sınırlandırılamayan sorumluluklar ile "
       "tüketici mevzuatından doğan haklarınız saklıdır."),
    _h2("10. Hesabın kapatılması"),
    _p('Hesabınızı istediğiniz zaman kapatabilirsiniz. Silme süreci <a href="/gizlilik/#hesap-silme">Gizlilik '
       "Politikası</a>'nda açıklanmıştır."),
    _h2("11. Değişiklikler"),
    _p("Bu koşulları güncelleyebiliriz. Önemli değişiklikleri yürürlüğe girmeden önce uygulama içinden bildiririz."),
    _h2("12. Uygulanacak hukuk ve uyuşmazlıklar"),
    _p("Bu koşullar Türkiye Cumhuriyeti hukukuna tabidir. Tüketici sıfatıyla, mevzuattaki parasal sınırlar dahilinde "
       "tüketici hakem heyetlerine, bu sınırları aşan uyuşmazlıklarda tüketici mahkemelerine başvurabilirsiniz."),
    _h2("13. İletişim"),
    CONTROLLER_BLOCK,
])

LEGAL = [
    dict(path="/gizlilik/", title="Gizlilik Politikası | Dozunda", h1="Gizlilik Politikası",
         description="Dozunda'nın hangi bilgilerinizi topladığı, nasıl kullandığı, kimlerle paylaştığı ve nasıl koruduğu. Hesap ve veri silme.",
         lead="Sağlık verisi hassastır. Neyi neden topladığımızı açıkça anlatıyoruz.", body=PRIVACY),
    dict(path="/kvkk/", title="KVKK Aydınlatma Metni | Dozunda", h1="KVKK Aydınlatma Metni",
         description="6698 sayılı KVKK kapsamında Dozunda'da işlenen kişisel veriler, işleme amaçları, hukuki sebepler, aktarım ve haklarınız.",
         lead="6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında bilgilendirme.", body=KVKK),
    dict(path="/acik-riza/", title="Sağlık Verileri Açık Rıza Metni | Dozunda", h1="Sağlık verileri açık rıza metni",
         description="Dozunda'da sağlık verilerinizin işlenmesine ilişkin açık rıza metni ve rızanızı geri alma yolları.",
         lead="Sağlık verileriniz yalnızca bu metindeki amaçlarla ve sizin açık rızanızla işlenir.", body=CONSENT),
    dict(path="/kullanim-kosullari/", title="Kullanım Koşulları | Dozunda", h1="Kullanım Koşulları",
         description="Dozunda mobil uygulaması ve web sitesinin kullanım koşulları, sağlık uyarısı, üyelik ve sorumluluklar.",
         lead="Dozunda'yı kullanmadan önce lütfen okuyun.", body=TERMS),
]
