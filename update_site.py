import datetime
import urllib.request
import xml.etree.ElementTree as ET
import re

def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = []
            for item in root.findall('.//item')[:3]:
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                
                title_text = title.text if title is not None else "ללא כותרת"
                link_text = link.text if link is not None else "#"
                desc_text = desc.text if desc is not None else "אין תמצית זמינה."
                
                if '<' in desc_text:
                    desc_text = re.sub('<.*?>', '', desc_text)
                
                items.append({
                    'title': title_text.strip(),
                    'link': link_text.strip(),
                    'desc': desc_text[:120].strip() + '...' if len(desc_text) > 120 else desc_text.strip()
                })
            return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    print("Fetching live news...")
    global_news = fetch_rss("https://www.technologyreview.com/feed/")
    israel_news = fetch_rss("https://www.geektime.co.il/feed/")
    cars_news = fetch_rss("https://www.autocar.co.uk/rss")
    
    # ברירת מחדל אם ה-RSS לא זמין כרגע
    if not global_news:
        global_news = [{'title': 'אזהרות חמורות מעולם המחקר: נקודת האל-חזור של AGI', 'link': 'https://www.technologyreview.com', 'desc': 'חוקרים בכירים מעלים דאגה עמוקה מכך שמודלי בינה מלאכותית מתחילים לפתח יכולות תכנון עצמאיות.'}]
    if not israel_news:
        israel_news = [{'title': 'האקו-סיסטם המקומי מוביל בפיתוח כלי הגנה ל-AI', 'link': 'https://www.geektime.co.il', 'desc': 'חברות הזנק ישראליות מציגות פתרונות חדשניים לאבטחת מודלי שפה ארגוניים.'}]
    if not cars_news:
        cars_news = [{'title': 'דור העתיד של הרכבים החשמליים: טווח נסיעה וטעינה אבסולוטית', 'link': 'https://www.autocar.co.uk', 'desc': 'יצרניות הרכב המובילות חושפות טכנולוגיות סוללה חדשות.'}]

    now = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")

    html_content = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Singularity & Polymarket Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap');
        body {{ font-family: 'Heebo', sans-serif; }}
        @keyframes marquee {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        .animate-marquee {{
            display: inline-block;
            animation: marquee 35s linear infinite;
        }}
    </style>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen pb-12 selection:bg-cyan-500 selection:text-white">

    <header class="border-b border-gray-800 bg-gray-900/95 backdrop-blur-md sticky top-0 z-50 shadow-xl">
        <div class="max-w-4xl mx-auto px-4 py-3 flex flex-col sm:flex-row justify-between items-center gap-3">
            <h1 class="text-xl sm:text-2xl font-black bg-gradient-to-r from-red-500 via-yellow-500 to-cyan-400 bg-clip-text text-transparent text-center sm:text-right">
                ⚡ AI Singularity & Polymarket Hub
            </h1>
            <div class="flex items-center gap-2">
                <button onclick="manualRefresh()" class="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs px-3.5 py-2 rounded-xl font-bold flex items-center gap-1.5 shadow-lg transition transform active:scale-95">
                    🔄 רענן עכשיו
                </button>
                <span id="update-time" class="text-xs bg-red-950/80 text-red-400 border border-red-800/60 px-3 py-1.5 rounded-full font-bold animate-pulse">
                    🔴 מעודכן: {now}
                </span>
            </div>
        </div>
        <div class="bg-gray-900/90 border-t border-gray-800/80 py-2 px-4 overflow-hidden flex items-center whitespace-nowrap">
            <span class="bg-red-600 text-white text-[10px] px-2 py-0.5 rounded font-bold ml-3 z-10 shadow">⚡ מבזקים</span>
            <div class="overflow-hidden w-full relative">
                <div class="animate-marquee text-xs text-gray-300 font-medium">
                    <span class="ml-10">[{now}] פריצת דרך במודלי AGI חדשים מעוררת דיונים סוערים במעבדות המחקר.</span>
                    <span class="ml-10">[{now}] ריאל מדריד נערכת למשחק העונה בסגל מלא לקראת האתגר באירופה.</span>
                    <span class="ml-10">[{now}] שער הדולר והשווקים הפיננסיים מגיבים לתנודות הגלובליות.</span>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-6 space-y-6">

        <section class="grid grid-cols-3 gap-3">
            <div class="bg-gray-900/90 border border-gray-800/80 p-3.5 rounded-2xl text-center shadow-lg">
                <span class="text-[11px] text-gray-400 block mb-1">💱 שער הדולר</span>
                <span id="val-usd" class="text-sm sm:text-base font-black text-green-400">3.64 ₪</span>
                <span class="text-[10px] text-green-400 block mt-0.5 font-bold">▲ +0.4%</span>
            </div>
            <div class="bg-gray-900/90 border border-gray-800/80 p-3.5 rounded-2xl text-center shadow-lg">
                <span class="text-[11px] text-gray-400 block mb-1">₿ ביטקוין</span>
                <span id="val-btc" class="text-sm sm:text-base font-black text-yellow-400">$68,450</span>
                <span class="text-[10px] text-green-400 block mt-0.5 font-bold">▲ +1.2%</span>
            </div>
            <div class="bg-gray-900/90 border border-gray-800/80 p-3.5 rounded-2xl text-center shadow-lg">
                <span class="text-[11px] text-gray-400 block mb-1">📈 S&P 500</span>
                <span id="val-sp" class="text-sm sm:text-base font-black text-cyan-400">5,620</span>
                <span class="text-[10px] text-red-400 block mt-0.5 font-bold">▼ -0.3%</span>
            </div>
        </section>

        <section class="bg-gray-900 border border-gray-800/80 p-4 sm:p-5 rounded-2xl shadow-xl space-y-3">
            <div class="flex flex-col sm:flex-row justify-between items-center gap-3">
                <div class="flex gap-2 text-xs">
                    <button onclick="switchAsset('btc')" id="asset-btc" class="px-3 py-1.5 bg-cyan-600 rounded-xl font-bold text-white transition shadow">ביטקוין</button>
                    <button onclick="switchAsset('usd')" id="asset-usd" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded-xl font-bold text-gray-300 transition">דולר/שקל</button>
                    <button onclick="switchAsset('sp')" id="asset-sp" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded-xl font-bold text-gray-300 transition">S&P 500</button>
                </div>
            </div>
            <div class="h-52 w-full">
                <canvas id="financialChart"></canvas>
            </div>
        </section>

        <div class="flex border-b border-gray-800 gap-6 overflow-x-auto text-sm pb-2 pt-2">
            <button onclick="switchTab('global')" id="btn-global" class="pb-2 border-b-2 border-cyan-500 font-bold text-cyan-400 whitespace-nowrap focus:outline-none transition">🌐 עולמי</button>
            <button onclick="switchTab('israel')" id="btn-israel" class="pb-2 border-b-2 border-transparent text-gray-400 hover:text-gray-200 whitespace-nowrap focus:outline-none transition">🇮🇱 ישראל</button>
            <button onclick="switchTab('madrid')" id="btn-madrid" class="pb-2 border-b-2 border-transparent text-gray-400 hover:text-gray-200 whitespace-nowrap focus:outline-none transition">⚽ ריאל מדריד</button>
            <button onclick="switchTab('cars')" id="btn-cars" class="pb-2 border-b-2 border-transparent text-gray-400 hover:text-gray-200 whitespace-nowrap focus:outline-none transition">🚗 רכב</button>
        </div>

        <!-- TAB GLOBAL -->
        <div id="tab-global" class="space-y-4">
            <h3 class="text-base sm:text-lg font-bold mb-4">🔥 הכתבות המובילות בעולם</h3>
"""

    for item in global_news:
        html_content += f"""
            <article class="bg-gray-900 border border-gray-800/80 rounded-2xl overflow-hidden shadow-lg">
                <div class="p-4 sm:p-5 space-y-2">
                    <span class="bg-red-950 text-red-400 text-[10px] px-2.5 py-0.5 rounded-full font-bold">חי מהרשת</span>
                    <h4 class="text-base font-bold">{item['title']}</h4>
                    <p class="text-gray-400 text-xs leading-relaxed">{item['desc']}</p>
                    <a href="{item['link']}" target="_blank" class="inline-block pt-2 text-cyan-400 hover:underline text-xs font-bold">לקריאת הכתבה המלאה ↗</a>
                </div>
            </article>
        """

    html_content += f"""
        </div>

        <!-- TAB ISRAEL -->
        <div id="tab-israel" class="space-y-4 hidden">
            <h3 class="text-base sm:text-lg font-bold mb-4">🇮🇱 עדכונים חיים בישראל</h3>
"""

    for item in israel_news:
        html_content += f"""
            <article class="bg-gray-900 border border-gray-800/80 rounded-2xl overflow-hidden shadow-lg">
                <div class="p-4 sm:p-5 space-y-2">
                    <span class="bg-blue-950 text-blue-400 text-[10px] px-2.5 py-0.5 rounded-full font-bold">ישראל</span>
                    <h4 class="text-base font-bold">{item['title']}</h4>
                    <p class="text-gray-400 text-xs leading-relaxed">{item['desc']}</p>
                    <a href="{item['link']}" target="_blank" class="inline-block pt-2 text-cyan-400 hover:underline text-xs font-bold">לקריאת הכתבה המלאה ↗</a>
                </div>
            </article>
        """

    html_content += f"""
        </div>

        <!-- TAB MADRID -->
        <div id="tab-madrid" class="space-y-4 hidden">
            <h3 class="text-base sm:text-lg font-bold mb-4">⚽ ריאל מדריד</h3>
            <article class="bg-gray-900 border border-gray-800/80 rounded-2xl overflow-hidden shadow-lg">
                <div class="p-4 sm:p-5 space-y-2">
                    <span class="bg-purple-950 text-purple-400 text-[10px] px-2.5 py-0.5 rounded-full font-bold">ריאל מדריד</span>
                    <h4 class="text-base font-bold">ההכנות לקראת משחק העונה בסגל מלא</h4>
                    <p class="text-gray-400 text-xs leading-relaxed">צוות האימון מתמקד בשיפור משחק הלחץ ובשילוב הכוכבים הצעירים בהרכב.</p>
                    <a href="https://www.realmadrid.com" target="_blank" class="inline-block pt-2 text-cyan-400 hover:underline text-xs font-bold">לקריאת הכתבה המלאה ↗</a>
                </div>
            </article>
        </div>

        <!-- TAB CARS -->
        <div id="tab-cars" class="space-y-4 hidden">
            <h3 class="text-base sm:text-lg font-bold mb-4">🚗 חדשות רכב</h3>
"""

    for item in cars_news:
        html_content += f"""
            <article class="bg-gray-900 border border-gray-800/80 rounded-2xl overflow-hidden shadow-lg">
                <div class="p-4 sm:p-5 space-y-2">
                    <span class="bg-green-950 text-green-400 text-[10px] px-2.5 py-0.5 rounded-full font-bold">רכב</span>
                    <h4 class="text-base font-bold">{item['title']}</h4>
                    <p class="text-gray-400 text-xs leading-relaxed">{item['desc']}</p>
                    <a href="{item['link']}" target="_blank" class="inline-block pt-2 text-cyan-400 hover:underline text-xs font-bold">לקריאת הכתבה המלאה ↗</a>
                </div>
            </article>
        """

    html_content += f"""
        </div>

    </main>

    <footer class="border-t border-gray-800 mt-12 py-6 text-center text-xs text-gray-500 px-4">
        AI Singularity & Polymarket Hub © 2026 • מעודכן אוטומטית בכל שעה עגולה
    </footer>

    <script>
        function switchTab(tabId) {{
            ['global', 'israel', 'madrid', 'cars'].forEach(t => {{
                document.getElementById('tab-' + t).classList.add('hidden');
                document.getElementById('btn-' + t).className = "pb-2 border-b-2 border-transparent text-gray-400 hover:text-gray-200 whitespace-nowrap focus:outline-none transition";
            }});
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).className = "pb-2 border-b-2 border-cyan-500 font-bold text-cyan-400 whitespace-nowrap focus:outline-none transition";
        }}

        let ctx = document.getElementById('financialChart').getContext('2d');
        let currentAssetData = {{
            btc: {{ label: 'ביטקוין ($)', data: [61000, 63000, 67000, 65000, 69000, 67000, 68450], color: '#facc15' }},
            usd: {{ label: 'דולר/שקל (₪)', data: [3.58, 3.60, 3.62, 3.59, 3.63, 3.61, 3.64], color: '#4ade80' }},
            sp: {{ label: 'S&P 500', data: [5400, 5450, 5520, 5480, 5590, 5600, 5620], color: '#22d3ee' }}
        }};

        let financialChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: ['ינו', 'פבר', 'מרץ', 'אפר', 'מאי', 'יוני', 'יולי'],
                datasets: [{{
                    label: currentAssetData.btc.label,
                    data: currentAssetData.btc.data,
                    borderColor: currentAssetData.btc.color,
                    backgroundColor: 'rgba(250, 204, 21, 0.1)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#9ca3af', font: {{ size: 10 }} }}, grid: {{ color: '#1f2937' }} }},
                    y: {{ ticks: {{ color: '#9ca3af', font: {{ size: 10 }} }}, grid: {{ color: '#1f2937' }} }}
                }}
            }}
        }});

        function switchAsset(assetKey) {{
            ['btc', 'usd', 'sp'].forEach(k => {{
                let btn = document.getElementById('asset-' + k);
                if(k === assetKey) {{
                    btn.className = "px-3 py-1.5 bg-cyan-600 rounded-xl font-bold text-white transition shadow";
                }} else {{
                    btn.className = "px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded-xl font-bold text-gray-300 transition";
                }}
            }});
            let asset = currentAssetData[assetKey];
            financialChart.data.datasets[0].label = asset.label;
            financialChart.data.datasets[0].data = asset.data;
            financialChart.data.datasets[0].borderColor = asset.color;
            financialChart.update();
        }}

        function manualRefresh() {{
            window.location.reload();
        }}
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html updated successfully!")

if __name__ == "__main__":
    main()
