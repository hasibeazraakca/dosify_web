"""
Dozunda web sitesinin alt sayfalarını (özellik sayfaları + blog) üretir.

Kullanım (depo kökünde):  python tools/build_pages.py
Çıktı: ilac-etkilesimi/, ilac-hatirlatici/, yakin-takibi/, nobetci-eczane/, blog/ klasörleri ve sitemap.xml

İçerik bu dosyadaki PAGES ve POSTS listelerindedir. Yeni blog yazısı eklemek için POSTS'a bir kayıt
ekleyip betiği yeniden çalıştırmak yeterli; menü, blog listesi, site haritası ve yapısal veri kendiliğinden güncellenir.

Sağlık içeriği kuralı: yazılar bilgilendirme amaçlıdır, belirli ilaç markası övülmez (reçeteli ilacın halka
tanıtımı yasak), tanı/tedavi önerisi verilmez; ilaca özgü yazılar yayından önce bir eczacı/hekime okutulur.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legal_content import LEGAL, META as LEGAL_META  # noqa: E402

SITE = "https://dozunda.com/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-09-21"
TODAY_TR = "21 Eylül 2026"

LEGAL_LINKS = [
    ("Gizlilik", "/gizlilik/"),
    ("KVKK Aydınlatma", "/kvkk/"),
    ("Açık rıza", "/acik-riza/"),
    ("Kullanım koşulları", "/kullanim-kosullari/"),
]

MENU = [
    ("İlaç etkileşimi", "/ilac-etkilesimi/"),
    ("İlaç hatırlatıcı", "/ilac-hatirlatici/"),
    ("Yakın takibi", "/yakin-takibi/"),
    ("Nöbetçi eczane", "/nobetci-eczane/"),
    ("Blog", "/blog/"),
]

DISCLAIMER = ("Bu sayfadaki bilgiler genel bilgilendirme amaçlıdır; tanı ve tedavi yerine geçmez. "
              "İlaçlarınızla ilgili kararları hekiminize veya eczacınıza danışarak verin. "
              "Hayati tehlike içeren acil durumlarda 112'yi arayın.")


# ---------------------------------------------------------------- küçük yardımcılar
def e(text):
    return html.escape(text, quote=True)


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def h3(text):
    return f"<h3>{text}</h3>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def steps(items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def faq_html(faq):
    if not faq:
        return ""
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    return f'<h2>Sıkça sorulanlar</h2><div class="faq">{items}</div>'


def cta():
    return ('<div class="cta"><h2>Dozunda çok yakında Google Play\'de</h2>'
            '<p>Üye olmadan ilaç etkileşimi kontrolü, ilaç hatırlatıcı, yakın takibi ve nöbetçi eczane — ücretsiz.</p>'
            '<a href="/#basvuru">Yayına çıkınca haber alın</a></div>')


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def breadcrumb_ld(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE.rstrip("/") + url}
            for i, (name, url) in enumerate(trail)
        ],
    }


def layout(*, path, title, description, h1, lead, body, trail, extra_ld=(), meta_line="", faq=None, related=(), legal=False):
    url = SITE.rstrip("/") + path
    menu = "".join(
        f'<a href="{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{n}</a>' for n, u in MENU
    )
    crumbs = " › ".join(
        (f'<a href="{u}">{e(n)}</a>' if i < len(trail) - 1 else e(n)) for i, (n, u) in enumerate(trail)
    )
    related_html = ""
    if related:
        links = "".join(f'<a href="{u}">{e(n)}<span>{e(d)}</span></a>' for n, u, d in related)
        related_html = f'<h2>Bunlar da ilginizi çekebilir</h2><div class="related">{links}</div>'
    lds = [breadcrumb_ld(trail), *extra_ld]
    if faq:
        lds.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
        })
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<title>{e(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="{e(description)}" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
<meta name="theme-color" content="#004D57" />
<link rel="icon" type="image/png" sizes="192x192" href="/favicon.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="stylesheet" href="/assets/site.css" />
<meta property="og:type" content="{"article" if path.startswith("/blog/") and path != "/blog/" else "website"}" />
<meta property="og:locale" content="tr_TR" />
<meta property="og:site_name" content="Dozunda" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(description)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
{"".join(ld(o) for o in lds)}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><img src="/favicon.png" alt="" width="30" height="30" />Dozunda</a>
  <nav class="menu" aria-label="Ana menü">{menu}</nav>
</div></header>
<main class="wrap">
  <nav class="crumbs" aria-label="Konum">{crumbs}</nav>
  <article>
    <h1>{h1}</h1>
    {f'<div class="meta">{meta_line}</div>' if meta_line else ''}
    <p class="lead">{lead}</p>
    {body}
    {faq_html(faq)}
    {'' if legal else f'<div class="note">{DISCLAIMER}</div>'}
    {'' if legal else cta()}
    {related_html}
  </article>
</main>
<footer class="foot"><div class="wrap">
  <div>{"".join(f'<a href="{u}">{n}</a>' for n, u in MENU)}<a href="/#sss">SSS</a><a href="/#basvuru">İletişim</a></div>
  <div>{"".join(f'<a href="{u}">{n}</a>' for n, u in LEGAL_LINKS)}</div>
  <div>© 2026 Dozunda · Cebinizdeki sağlık asistanı</div>
</div></footer>
</body>
</html>
"""


# ---------------------------------------------------------------- özellik sayfaları
FEATURE_LINKS = {
    "etkilesim": ("İlaç etkileşimi sorgulama", "/ilac-etkilesimi/", "İlaçlarınız birbiriyle uyumlu mu?"),
    "hatirlatici": ("İlaç hatırlatıcı", "/ilac-hatirlatici/", "Dozunuzu zamanında alın"),
    "yakin": ("Yakın takibi", "/yakin-takibi/", "Anne babanızın ilacını uzaktan takip edin"),
    "nobetci": ("Nöbetçi eczane", "/nobetci-eczane/", "İl ve ilçeye göre açık eczane"),
}

PAGES = [
    dict(
        path="/ilac-etkilesimi/",
        title="İlaç Etkileşimi Sorgulama: Ücretsiz ve Üyeliksiz | Dozunda",
        description="Kullandığınız ilaçların birbiriyle etkileşimini üye olmadan, saniyeler içinde kontrol edin. "
                    "İlaç adını yazın ya da kutudaki karekodu okutun. Ücretsiz.",
        h1="İlaç etkileşimi sorgulama",
        lead="Birden fazla ilaç kullanıyorsanız, ilaçlarınızın birbiriyle uyumlu olup olmadığını Dozunda ile üye "
             "olmadan, saniyeler içinde kontrol edebilirsiniz.",
        body="".join([
            h2("İlaç etkileşimi nedir?"),
            p("İlaç etkileşimi, iki ya da daha fazla ilacın birlikte kullanıldığında birbirinin etkisini artırması, "
              "azaltması ya da beklenmeyen yan etkilere yol açması durumudur. Özellikle farklı hekimlerden ilaç "
              "yazılan, kronik hastalığı olan ya da reçetesiz ağrı kesici ve takviyeleri reçeteli ilaçlarıyla "
              "birlikte kullanan kişilerde dikkat edilmesi gereken bir konudur."),
            h2("Dozunda ile nasıl kontrol edilir?"),
            steps([
                "<b>İlk ilacı ekleyin.</b> İlacın adını yazın ya da ilaç kutusundaki karekodu telefonunuzun kamerasıyla okutun.",
                "<b>Diğer ilacı ekleyin.</b> Birlikte kullandığınız ikinci ilacı aynı şekilde seçin.",
                "<b>Sonucu görün.</b> Dozunda, bilinen bir etkileşim varsa önem derecesiyle birlikte gösterir.",
            ]),
            p("Üye olursanız kayıtlı ilaçlarınızı tek seferde birlikte kontrol edebilir, sonuçları ilaç "
              "hatırlatıcınızla birlikte kullanabilirsiniz. Üye olmadan da tek tek sorgulama yapabilirsiniz."),
            h2("Sonucu nasıl değerlendirmeliyim?"),
            p("Etkileşim sonucu bir uyarıdır, tek başına bir karar değildir. Bir etkileşim görürseniz ilacınızı "
              "kendi başınıza bırakmayın ya da dozunu değiştirmeyin; sonucu eczacınıza veya hekiminize gösterin. "
              "Etkileşim görmemeniz de iki ilacın her durumda güvenli olduğu anlamına gelmez."),
        ]),
        faq=[
            ("İlaç etkileşimi sorgulamak ücretli mi?", "Hayır. Dozunda'da ilaç etkileşimi kontrolü ücretsizdir ve üyelik gerektirmez."),
            ("Karekod okutarak ilaç ekleyebilir miyim?", "Evet. İlaç kutusundaki karekodu telefonunuzun kamerasıyla okutarak ilacı listeye ekleyebilirsiniz."),
            ("Etkileşim çıkarsa ilacımı bırakmalı mıyım?", "Hayır, kendi başınıza ilacınızı bırakmayın ya da dozunu değiştirmeyin. Sonucu eczacınıza veya hekiminize danışın."),
            ("Reçetesiz ilaçları ve takviyeleri de kontrol edebilir miyim?", "Veri tabanında bulunan reçetesiz ilaçları da sorgulayabilirsiniz. Kullandığınız her ürünü eczacınıza söylemeniz yine de önemlidir."),
        ],
        related=[FEATURE_LINKS["hatirlatici"], FEATURE_LINKS["yakin"]],
    ),
    dict(
        path="/ilac-hatirlatici/",
        title="İlaç Hatırlatıcı Uygulaması: Dozunuzu Unutmayın | Dozunda",
        description="İlaç saatinde hatırlatma alın, kutuda kalan ilacı takip edin, kronik ilaçta reçete zamanını "
                    "kaçırmayın. Kendiniz ve aileniz için ücretsiz.",
        h1="İlaç hatırlatıcı",
        lead="Dozunda, ilacınızı zamanında almanız için doz saatinde hatırlatır, kutuda kalan ilacı sayar ve ilacınız "
             "bitmeden sizi uyarır.",
        body="".join([
            h2("Neler yapabilirsiniz?"),
            ul([
                "<b>Günde birden fazla doz:</b> Sabah, öğle, akşam gibi istediğiniz kadar saat ekleyin.",
                "<b>Belirli günler:</b> Her gün değil de haftanın belirli günlerinde kullanılan ilaçlar için gün seçin.",
                "<b>Kutuda kalan adet:</b> Her dozu işaretlediğinizde kalan sayı düşer; azaldığında uyarı alırsınız.",
                "<b>Kronik ilaçlar:</b> Sürekli kullandığınız ilacın kutusu biterken reçetenizi yazdırmayı hatırlatır.",
                "<b>Geçmiş:</b> Önceki günlerde hangi dozu aldığınızı görün, unuttuğunuzu işaretleyin.",
                "<b>Aileniz için:</b> Çocuğunuz ya da bakımını üstlendiğiniz bir yakınınız için ayrı profil açın.",
            ]),
            h2("Nasıl kurulur?"),
            steps([
                "Ücretsiz üye olun ve Hatırlatıcı sekmesine girin.",
                "İlacın adını yazın ya da kutudaki karekodu okutun.",
                "Doz saatlerini, sıklığı ve isterseniz kutudaki adet sayısını girin.",
            ]),
            p("Doz saati geldiğinde bildirim alırsınız. İlacınızı aldığınızda tek dokunuşla işaretlemeniz yeterli."),
            h2("Anne babanızın ilacını da takip edin"),
            p("Yakınınız kendi telefonunda Dozunda kullanıyorsa, onun onayıyla dozlarını aldığını kendi telefonunuzdan "
              f'görebilirsiniz. Ayrıntılar için <a href="/yakin-takibi/">yakın takibi</a> sayfasına bakın.'),
        ]),
        faq=[
            ("İlaç hatırlatıcı ücretli mi?", "Hayır, Dozunda'nın ilaç hatırlatıcısı ücretsizdir."),
            ("Bir dozu unutursam ne olur?", "Doz saatinden sonra işaretlenmeyen doz, geçmişinizde alınmadı olarak görünür. Unutulan bir doz için ne yapılacağı ilaca göre değişir; kullanma talimatına bakın ya da eczacınıza sorun."),
            ("Aynı anda birden fazla ilaç ekleyebilir miyim?", "Evet, istediğiniz kadar ilaç ve doz saati ekleyebilirsiniz."),
            ("Ailemdeki biri için hatırlatıcı kurabilir miyim?", "Evet. Aile üyesi profili ekleyip onun ilaçları için ayrı hatırlatıcı kurabilirsiniz."),
        ],
        related=[FEATURE_LINKS["yakin"], FEATURE_LINKS["etkilesim"]],
    ),
    dict(
        path="/yakin-takibi/",
        title="Yaşlı Anne Babanın İlaç Takibi: Yakın Takibi | Dozunda",
        description="Annenizin, babanızın ilacını zamanında aldığını telefonunuzdan görün; almadıysa tek dokunuşla "
                    "hatırlatın. Onaya dayalı, güvenli ve ücretsiz yakın takibi.",
        h1="Yakın takibi: anne babanızın ilacını uzaktan görün",
        lead="\"İlacını içtin mi?\" diye her gün aramanıza gerek yok. Yakınınız ilacını aldığında Dozunda'da görürsünüz; "
             "almadıysa tek dokunuşla hatırlatırsınız.",
        body="".join([
            h2("Nasıl çalışır?"),
            steps([
                "<b>Yakınınız kod oluşturur.</b> Kendi telefonunda Profil › Yakınlarım bölümünden 6 karakterli bir eşleştirme kodu oluşturur. Kod 10 dakika geçerlidir ve tek kullanımlıktır.",
                "<b>Siz kodu girersiniz.</b> Kendi Dozunda uygulamanızda Yakınlarım bölümüne kodu yazar, yakınınıza bir isim verirsiniz (ör. Annem).",
                "<b>Yakınınız onaylar.</b> Kendi telefonunda neleri görebileceğinizi okur ve onaylar. Onay olmadan hiçbir bilgi paylaşılmaz.",
                "<b>Dozları görürsünüz.</b> Hatırlatıcı ekranında yakınınızı seçerek bugün hangi dozu aldığını, hangisini beklediğini ya da kaçırdığını görürsünüz.",
            ]),
            h2("Almadıysa hatırlatın"),
            p("Saati gelmiş ama henüz alınmamış bir dozun yanında \"Hatırlat\" butonu çıkar. Dokunduğunuzda yakınınızın "
              "telefonuna \"ilacınızı almayı unutmayın\" bildirimi gider. Yakınınız bildirimden tek dokunuşla \"Aldım\" diyebilir."),
            h2("Gizlilik"),
            ul([
                "Yalnızca hatırlatıcılar ve doz bilgisi paylaşılır; alerji, kronik hastalık gibi diğer sağlık bilgileri paylaşılmaz.",
                "Paylaşım yakınınızın açık onayıyla başlar; yakınınız onayını istediği an geri alabilir.",
                "İki taraf da bağlantıyı istediği zaman kaldırabilir; erişim anında kapanır.",
            ]),
        ]),
        faq=[
            ("Yakınımın telefonunda da Dozunda olması gerekiyor mu?", "Evet. Yakın takibi, iki tarafın da kendi Dozunda hesabıyla çalışır. Yakınınızın telefonu yoksa onun için aile üyesi profili açıp hatırlatıcıları kendi telefonunuzda yönetebilirsiniz."),
            ("Yakınım neleri paylaşmış olur?", "Yalnızca hatırlatıcıları ve dozlarını aldığı bilgisini. Diğer sağlık bilgileri paylaşılmaz."),
            ("Bu özellik ücretli mi?", "Hayır, yakın takibi ve aile özellikleri ücretsizdir."),
            ("Takibi nasıl sonlandırırım?", "İki taraf da Profil › Yakınlarım bölümünden bağlantıyı tek dokunuşla kaldırabilir."),
        ],
        related=[FEATURE_LINKS["hatirlatici"], ("Yaşlı anne babanın ilaç takibi: 6 pratik yol", "/blog/yasli-anne-babanin-ilac-takibi/", "Blog yazısı")],
    ),
    dict(
        path="/nobetci-eczane/",
        title="Nöbetçi Eczane Bul: İl ve İlçeye Göre | Dozunda",
        description="Gece, hafta sonu ve bayramda açık nöbetçi eczaneyi il ve ilçenize göre bulun. Türkiye'nin 81 ili. Ücretsiz, üyelik gerektirmez.",
        h1="Nöbetçi eczane bul",
        lead="Dozunda'da il ve ilçenizi seçin, o günün nöbetçi eczanelerini görün. Türkiye'nin 81 ili için, üye olmadan.",
        body="".join([
            h2("Nasıl kullanılır?"),
            steps([
                "Eczane sekmesini açın.",
                "İlinizi seçin; listeden seçebilir ya da adını yazabilirsiniz.",
                "İsterseniz ilçenizi seçin; nöbetçi eczaneler adres ve telefonlarıyla listelenir.",
            ]),
            h2("Gitmeden önce"),
            ul([
                "Nöbet listeleri il eczacı odalarından alınır; değişiklik olabileceği için yola çıkmadan önce eczaneyi arayın.",
                "E-reçeteniz varsa reçete numarasını ve kimliğinizi yanınıza alın.",
                "Hayati tehlike içeren acil durumlarda eczane aramak yerine 112'yi arayın.",
            ]),
            p('Nöbetçi eczanelerle ilgili daha fazla bilgi için <a href="/blog/nobetci-eczane-nasil-bulunur/">'
              "Nöbetçi eczane nasıl bulunur?</a> yazımıza bakın."),
        ]),
        faq=[
            ("Nöbetçi eczane listesi nereden geliyor?", "Liste, il eczacı odalarının yayımladığı nöbet çizelgelerinden alınır."),
            ("Nöbetçi eczane bulmak için üye olmam gerekir mi?", "Hayır, nöbetçi eczane araması üyelik gerektirmez."),
            ("Hangi illerde çalışıyor?", "Türkiye'nin 81 ilinde il ve ilçeye göre arama yapabilirsiniz."),
        ],
        related=[("Nöbetçi eczane nasıl bulunur?", "/blog/nobetci-eczane-nasil-bulunur/", "Blog yazısı"), FEATURE_LINKS["etkilesim"]],
    ),
]


# ---------------------------------------------------------------- blog yazıları
POSTS = [
    dict(
        slug="prospektus-karekod-elektronik-kullanma-talimati",
        title="İlaç kutularında prospektüs kalkıyor mu? Karekodla e-KT rehberi",
        h1="İlaç kutularında prospektüs kalkıyor mu? Karekodla elektronik kullanma talimatı (e-KT) rehberi",
        seo_title="Prospektüs kalkıyor mu? Karekodla e-KT rehberi",
        description="Kâğıt prospektüs yerine karekodla açılan elektronik kullanma talimatı (e-KT) geliyor. "
                    "Ne değişiyor, nasıl okutulur, basılı talimat istenebilir mi?",
        summary="Basılı prospektüs yerine karekodla açılan elektronik kullanma talimatı geliyor. Ne değişiyor, nasıl kullanılır?",
        lead="İlaç kutularından çıkan kâğıt prospektüs yerini kutudaki karekodla açılan elektronik kullanma "
             "talimatına (e-KT) bırakıyor. Bu yazıda neyin değiştiğini ve talimata nasıl ulaşacağınızı anlatıyoruz.",
        body="".join([
            h2("Ne değişiyor?"),
            p("Türkiye İlaç ve Tıbbi Cihaz Kurumu'nun (TİTCK) 6 Aralık 2024'te yayımladığı kılavuzla elektronik "
              "kullanma talimatına geçiş başladı. Basında yer alan haberlere göre 1 Ocak 2027'den itibaren, istisna "
              "tutulan ürünler dışındaki ilaçlarda e-KT kullanımı zorunlu olacak ve basılı kullanma talimatının kutuda "
              "bulunması isteğe bağlı hale gelecek."),
            h2("Elektronik kullanma talimatı (e-KT) nedir?"),
            p("e-KT, ilacın onaylı kullanma talimatının dijital halidir. Kutunun üzerindeki karekodu telefonunuzla "
              "okuttuğunuzda talimata ulaşırsınız. Talimatta bir güncelleme yapıldığında dijital sürüm de güncellenir; "
              "yani elinizdeki bilgi kutunun üretildiği tarihte kalmaz."),
            h2("Nasıl okutulur?"),
            steps([
                "Telefonunuzun kamerasını ya da karekod okuyucusunu açın.",
                "Kamerayı ilaç kutusunun dış yüzündeki karekoda tutun.",
                "Açılan bağlantıdan ilacın güncel kullanma talimatını okuyun.",
            ]),
            h2("Basılı talimat isteyebilir miyim?"),
            p("Haberlere göre talep eden hastalara basılı kullanma talimatı sunulmaya devam edilebilecek. Basılı "
              "talimata ihtiyacınız varsa eczacınıza sorun."),
            h2("Karekod açılmazsa ne yapmalıyım?"),
            p("Kutuda basılı talimat yoksa ve karekod üzerinden talimata ulaşamıyorsanız, ilacın ruhsat sahibi "
              "firmasıyla iletişime geçmeniz öneriliyor. Firma bilgileri ilacın kutusunda yer alır. Eczacınız da "
              "bu konuda yardımcı olabilir."),
            h2("Yaşlı yakınlarınız için birkaç öneri"),
            ul([
                "Karekodu okutmayı bir kez birlikte deneyin; yazı boyutunu büyütmeyi gösterin.",
                "Sık kullanılan ilaçların talimatındaki doz ve uyarı bölümlerini birlikte okuyun.",
                "Emin olunamayan her konuda eczacıya danışmayı alışkanlık haline getirin.",
            ]),
            h2("Dozunda bu konuda ne yapar?"),
            p("Dozunda'da ilaç kutusundaki karekodu okutarak ilacı bulabilir, kullandığınız diğer ilaçlarla "
              f'<a href="/ilac-etkilesimi/">etkileşimini kontrol edebilir</a> ve '
              f'<a href="/ilac-hatirlatici/">hatırlatıcı kurabilirsiniz</a>.'),
            '<p class="sources">Kaynaklar: basında yer alan haberler (Eylül 2026) — '
            '<a href="https://www.trtv.net/2026/09/18/ilac-kutularinda-elektronik-kullanma-talimati-2027/" rel="nofollow noopener">TR Haberleri</a>, '
            '<a href="https://www.aydinlik.com.tr/haber/ilac-kutularinda-yeni-donem-prospektusler-dijital-ortama-tasiniyor-590815" rel="nofollow noopener">Aydınlık</a>. '
            "Kesin tarih ve istisnalar için TİTCK duyurularını takip edin.</p>",
        ]),
    ),
    dict(
        slug="nobetci-eczane-nasil-bulunur",
        title="Nöbetçi eczane nasıl bulunur? Gece, hafta sonu ve bayram rehberi",
        h1="Nöbetçi eczane nasıl bulunur? Gece, hafta sonu ve bayramda eczane rehberi",
        seo_title="Nöbetçi eczane nasıl bulunur? Gece ve bayram rehberi",
        description="Gece, hafta sonu ve bayramda açık eczaneyi bulmanın yolları ve nöbetçi eczaneye "
                    "gitmeden önce bilmeniz gerekenler.",
        summary="Mesai dışında açık eczaneyi bulmanın yolları ve gitmeden önce bilmeniz gerekenler.",
        lead="Eczanelerin kapalı olduğu saatlerde ilaca ihtiyaç duyduğunuzda nöbetçi eczaneyi nasıl bulacağınızı ve "
             "gitmeden önce nelere dikkat etmeniz gerektiğini derledik.",
        body="".join([
            h2("Nöbetçi eczane nedir?"),
            p("Nöbetçi eczaneler, eczanelerin mesai saatleri dışında — gece, hafta sonu ve resmi tatillerde — sırayla "
              "açık kalan eczanelerdir. Nöbet çizelgeleri il eczacı odaları tarafından düzenlenir. Nöbet saatleri ile ve "
              "güne göre değişebilir; genellikle akşam saatlerinde başlar ve ertesi sabah sona erer."),
            h2("Nöbetçi eczaneyi bulmanın 3 yolu"),
            h3("1. Uygulamadan il ve ilçeye göre arayın"),
            p(f'<a href="/nobetci-eczane/">Dozunda\'da</a> il ve ilçenizi seçerek o günün nöbetçi eczanelerini adres ve '
              "telefonlarıyla görebilirsiniz. Üyelik gerekmez."),
            h3("2. İl eczacı odasının internet sitesine bakın"),
            p("Her ilin eczacı odası güncel nöbet listesini yayımlar."),
            h3("3. Kapalı eczanelerin kapısına bakın"),
            p("Kapalı eczaneler genellikle o günün nöbetçi eczanelerini kapılarında ya da vitrinlerinde gösterir."),
            h2("Gitmeden önce"),
            ul([
                "<b>Arayın:</b> Nöbet listelerinde değişiklik olabilir; eczanenin açık olduğundan emin olun.",
                "<b>Reçetenizi hazırlayın:</b> E-reçeteniz varsa reçete numarasını ve kimliğinizi yanınıza alın.",
                "<b>İlacın adını bilin:</b> Kullandığınız ilacın kutusunu ya da fotoğrafını götürmek işinizi kolaylaştırır.",
            ]),
            h2("Acil durumlarda"),
            p("Nefes darlığı, bilinç kaybı, şiddetli göğüs ağrısı gibi hayati tehlike içeren durumlarda eczane aramakla "
              "zaman kaybetmeyin; 112 Acil Çağrı Merkezi'ni arayın."),
        ]),
    ),
    dict(
        slug="yasli-anne-babanin-ilac-takibi",
        title="Yaşlı anne babanın ilaç takibi: 6 pratik yol",
        h1="Yaşlı anne babanızın ilaçlarını takip etmenin 6 pratik yolu",
        description="Anne babanızın ilaçlarını düzenli ve güvenli almasına yardımcı 6 yöntem: ilaç listesi, "
                    "haftalık kutu, hatırlatıcı, stok, etkileşim ve uzaktan takip.",
        summary="İlaç listesinden uzaktan takibe, anne babanızın ilaçlarını düzenli almasına yardımcı 6 yöntem.",
        lead="Yaş ilerledikçe kullanılan ilaç sayısı artar, takip zorlaşır. Anne babanızın ilaçlarını düzenli ve "
             "güvenli almasına yardımcı olacak 6 pratik yöntemi derledik.",
        body="".join([
            h2("1. Güncel bir ilaç listesi tutun"),
            p("Her ilacın adını, dozunu, hangi saatte alındığını, ne için kullanıldığını ve hangi hekimin yazdığını "
              "tek bir listede toplayın. Bu listeyi her doktor kontrolüne götürün; farklı hekimlerin yazdığı ilaçlar "
              "arasındaki ilişkiyi görmek kolaylaşır."),
            h2("2. Haftalık ilaç kutusu kullanın"),
            p("Günlere ve saatlere bölünmüş ilaç kutuları, bir dozun alınıp alınmadığını bir bakışta görmeyi sağlar. "
              "Kutuyu haftada bir, sakin bir zamanda birlikte doldurmak hata riskini azaltır."),
            h2("3. Hatırlatıcı kurun"),
            p(f'Telefon alarmı ya da bir <a href="/ilac-hatirlatici/">ilaç hatırlatıcı</a> doz saatlerini unutmayı '
              "önler. Birden fazla ilaç ve saat varsa ilaç adıyla hatırlatan bir uygulama alarmdan daha kullanışlıdır."),
            h2("4. Kutuda kalan ilacı takip edin"),
            p("Sürekli kullanılan ilaçların bitmesi, özellikle reçete yenileme gerektiğinde sorun olur. Kalan adeti "
              "takip edin; ilaç bitmeden hekim randevusunu ya da reçeteyi ayarlayın."),
            h2("5. İlaç etkileşimlerine dikkat edin"),
            p("Farklı hekimlerden ilaç yazılması, reçetesiz ağrı kesiciler ve takviyeler etkileşim riskini artırabilir. "
              f'Yeni bir ilaç eklendiğinde <a href="/ilac-etkilesimi/">etkileşim kontrolü</a> yapın ve eczacıya '
              "kullanılan tüm ilaçları söyleyin."),
            h2("6. Uzaktan takip edin"),
            p(f'Aynı evde yaşamıyorsanız <a href="/yakin-takibi/">yakın takibi</a> ile anne babanızın onayıyla ilacını '
              "aldığını telefonunuzdan görebilir, almadıysa tek dokunuşla hatırlatabilirsiniz. Her gün \"ilacını içtin "
              "mi?\" diye aramak yerine yalnızca gerektiğinde devreye girersiniz."),
            h2("Önemli bir not: unutulan doz"),
            p("Bir doz unutulduğunda ne yapılacağı ilaçtan ilaca değişir. Unutulan dozu telafi etmek için ikinci dozu "
              "birlikte almak bazı ilaçlarda risklidir. Kullanma talimatına bakın ya da eczacınıza danışın."),
        ]),
    ),
]


# ---------------------------------------------------------------- üretim
def write(rel_dir, content):
    folder = os.path.join(ROOT, rel_dir.strip("/"))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def build():
    urls = [("/", "1.0")]
    for page in PAGES:
        trail = [("Ana sayfa", "/"), (page["h1"].split(":")[0], page["path"])]
        write(page["path"], layout(trail=trail, meta_line="", **{k: v for k, v in page.items()}))
        urls.append((page["path"], "0.9"))

    for post in POSTS:
        path = f"/blog/{post['slug']}/"
        trail = [("Ana sayfa", "/"), ("Blog", "/blog/"), (post["title"], path)]
        article_ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post["title"],
            "description": post["description"],
            "inLanguage": "tr",
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": {"@type": "Organization", "name": "Dozunda Editör Ekibi", "url": SITE},
            "publisher": {"@type": "Organization", "name": "Dozunda", "logo": {"@type": "ImageObject", "url": SITE + "favicon.png"}},
            "image": SITE + "og-image.png",
            "mainEntityOfPage": SITE.rstrip("/") + path,
        }
        write(path, layout(
            path=path, title=f"{post.get('seo_title', post['title'])} | Dozunda", description=post["description"],
            h1=post["h1"], lead=post["lead"], body=post["body"], trail=trail, extra_ld=[article_ld],
            meta_line=f"Dozunda Editör Ekibi · Son güncelleme: {TODAY_TR}",
            related=[(o["title"], f"/blog/{o['slug']}/", o["summary"]) for o in POSTS if o is not post][:2],
        ))
        urls.append((path, "0.7"))

    for doc in LEGAL:
        write(doc["path"], layout(
            path=doc["path"], title=doc["title"], description=doc["description"], h1=doc["h1"],
            lead=doc["lead"], body=doc["body"], trail=[("Ana sayfa", "/"), (doc["h1"], doc["path"])],
            meta_line=LEGAL_META, legal=True,
        ))
        urls.append((doc["path"], "0.3"))

    posts_html = '<div class="posts">' + "".join(
        f'<a href="/blog/{o["slug"]}/"><b>{e(o["title"])}</b><span>{e(o["summary"])}</span></a>' for o in POSTS
    ) + "</div>"
    write("/blog/", layout(
        path="/blog/", title="Blog: İlaç Kullanımı ve Sağlık Rehberleri | Dozunda",
        description="İlaç kullanımı, ilaç takibi, nöbetçi eczane ve sağlık okuryazarlığı üzerine anlaşılır rehberler.",
        h1="Dozunda Blog", lead="İlaçlarınızı güvenle kullanmanız için anlaşılır rehberler.",
        body=posts_html, trail=[("Ana sayfa", "/"), ("Blog", "/blog/")],
    ))
    urls.insert(1, ("/blog/", "0.8"))

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority in urls:
        sitemap.append(f"  <url><loc>{SITE.rstrip('/')}{path}</loc><lastmod>{TODAY}</lastmod><priority>{priority}</priority></url>")
    sitemap.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sitemap) + "\n")
    print(f"{len(PAGES)} özellik sayfası, {len(POSTS)} blog yazısı, blog ana sayfası ve {len(urls)} adresli site haritası üretildi.")


if __name__ == "__main__":
    build()
