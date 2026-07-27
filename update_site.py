import datetime
import urllib.request
import xml.etree.ElementTree as ET

def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = []
            for item in root.findall('.//item')[:3]:  # לוקח את 3 הכתבות המובילות
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                
                title_text = title.text if title is not None else "ללא כותרת"
                link_text = link.text if link is not None else "#"
                desc_text = desc.text if desc is not None else "אין תמצית זמינה."
                
                # ניקוי תגיות HTML מהתמצית אם יש
                if '<' in desc_text:
                    import re
                    desc_text = re.sub('<.*?>', '', desc_text)
                
                items.append({
                    'title': title_text,
                    'link': link_text,
                    'desc': desc_text[:120] + '...' if len(desc_text) > 120 else desc_text
                })
            return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    print("Starting automated news update...")
    
    # מקורות חדשות אמיתיים
    global_news = fetch_rss("https://www.technologyreview.com/feed/")
    israel_news = fetch_rss("https://www.geektime.co.il/feed/")
    cars_news = fetch_rss("https://www.autocar.co.uk/rss")
    
    now = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
    print(f"Fetched successfully at {now}")

if __name__ == "__main__":
    main()
