from pathlib import Path
from html import escape as E
import json,re
from urllib.parse import quote
ROOT=Path(__file__).parent;D=ROOT/'dist';A=D/'assets'
scholar='https://scholar.google.com/citations?hl=en&user=1auhR6QAAAAJ&view_op=list_works&sortby=pubdate'
logo='<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 42V21M24 30C8 32 5 21 6 10c12-1 22 4 18 20ZM24 23C24 9 33 5 43 5c1 12-5 20-19 18Z" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linejoin="round"/><path d="m12 17 12 13M35 13 24 24" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
nav=[('Home','index.html'),('Research','research.html'),('People','people.html'),('Publications','publications.html'),('Lab News','lab-news.html'),('Teaching','teaching.html'),('Resources','resources.html'),('Join us','opportunities.html')]
def link(url,text,cls=''):return f'<a class="{cls}" href="{url}">{text}</a>'
def page(name,title,body):
 links=''.join(f'<a href="{u}" {"aria-current=\"page\"" if name==u else ""}>{n}</a>' for n,u in nav)
 html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} | Engineering Biogeochemistry Lab · UCF</title><meta name="description" content="The Engineering Biogeochemistry Lab at the University of Central Florida explores biogeochemistry, wetlands, soil carbon, greenhouse gases, and water quality."><meta name="theme-color" content="#143d35"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script defer src="app.js{'?v=research-areas' if name=='publications.html' else ''}"></script></head><body><a class="skip" href="#main">Skip to content</a><div class="university"><div class="wrap"><span>UNIVERSITY OF CENTRAL FLORIDA</span><span>College of Engineering and Computer Science</span></div></div><header><div class="wrap header-inner"><a class="brand" href="index.html">{logo}<span>Engineering Biogeochemistry Lab<small>HU RESEARCH GROUP</small></span></a><button class="menu-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button><nav id="main-nav" aria-label="Main navigation">{links}<a class="nav-contact" href="contact.html" {"aria-current=\"page\"" if name=='contact.html' else ''}>Contact</a></nav></div></header><main id="main">{body}</main><footer><div class="wrap footer-top"><a class="brand" href="index.html">{logo}<span>Engineering Biogeochemistry Lab<small>HU RESEARCH GROUP · UCF</small></span></a><div><p>Engineering biogeochemistry.<br>Advancing environmental quality.</p></div><div><a href="mailto:jing.hu@ucf.edu">jing.hu@ucf.edu</a><p>Orlando, Florida</p></div></div><div class="wrap footer-bottom"><span>© 2026 Hu Research Group</span><div><a href="{scholar}" target="_blank" rel="noopener">Google Scholar</a><a href="https://www.cece.ucf.edu/" target="_blank" rel="noopener">UCF CECE</a><a href="contact.html">Contact</a></div></div></footer></body></html>'''
 (D/name).write_text(html)
def intro(label,title,desc=''):return f'<section class="page-intro"><div class="wrap"><p class="eyebrow">{label}</p><h1>{title}</h1><p class="lead">{desc}</p></div></section>'
def cta():return '<section class="cta"><div class="wrap cta-inner"><div><p class="eyebrow">GROW WITH US</p><h2>Bring your curiosity.<br>Make a difference.</h2></div><div><p>Explore opportunities to study soil, water, and the natural processes that connect them.</p><a class="button light" href="opportunities.html">Explore open positions</a></div></div></section>'
(A/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#143d35"/><path d="M24 40V24C8 28 7 16 8 10c12 0 17 6 16 14 0-15 7-18 17-18 0 12-6 20-17 18" fill="none" stroke="#d8e9b6" stroke-width="2"/></svg>')
from datetime import date
from itertools import groupby
news=sorted(json.loads((ROOT/'lab-news.json').read_text()),key=lambda item:item['date'],reverse=True)
# Write about the event in the lab’s voice; use the source link for attribution.
def news_story(item, compact=False):
 slug=E(item['id']); headline=E(item['title']); stamp=date.fromisoformat(item['date'])
 meta=f'<p class="eyebrow"><time datetime="{stamp.isoformat()}">{stamp:%B %Y}</time> · {E(item["category"])}</p>'
 if compact:
  return f'<article>{meta}<h3><a href="lab-news.html#{slug}">{headline}</a></h3><p>{E(item["summary"])}</p></article>'
 embed=''.join(
  f'<iframe src="{E(post["url"])}" width="504" height="{int(post["height"])}" style="display:block;max-width:100%;border:0" loading="lazy" allowfullscreen title="{headline} · LinkedIn post {index}"></iframe>'
  for index,post in enumerate(item.get('embeds',[]),1)
 )
 photo=item.get('photo')
 picture=f'<figure style="margin:1rem 0 0;max-width:360px"><img src="{E(photo["src"])}" width="{int(photo["width"])}" height="{int(photo["height"])}" alt="{E(photo["alt"])}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:5px"></figure>' if photo else ''
 source_link=f'<a class="text-link" href="{E(item["url"])}">View on LinkedIn</a>' if item.get('url') else ''
 return f'<article id="{slug}">{meta}<h3>{headline}</h3><p>{E(item["summary"])}</p>{picture}{embed}{source_link}</article>'
selected=sorted(news,key=lambda item:not item.get('featured',False))[:3]
home_news='<section class="section" id="lab-news"><div class="wrap intro-grid"><div><p class="eyebrow">FROM THE LAB</p><h2>Lab News</h2><a class="text-link" href="lab-news.html">View all lab news</a></div><div class="news-stories">'+''.join(news_story(item,True) for item in selected)+'</div></div></section>'
archive=intro('FROM THE LAB','Lab News','Meet our newest lab members, follow our fieldwork, and celebrate student milestones with us.')
for year,group in groupby(news,key=lambda item:item['date'][:4]):
 archive+=f'<section class="section"><div class="wrap intro-grid"><h2>{year}</h2><div class="news-stories">'+''.join(news_story(item) for item in group)+'</div></div></section>'
page('lab-news.html','Lab News',archive)
hero='assets/wetland-home.webp'
credit='Wetland research site'
# Shared labels and links for Home and Research.
research=[
 ('water','Nutrient Cycling and Water Quality','How do nitrogen and phosphorus move between soils and water, and which forms remain available to organisms?','Nitrogen · Phosphorus · Water quality'),
 ('wetlands','Nature-Based Water Treatment','How can we design and operate treatment wetlands to keep excess nutrients out of receiving waters?','Treatment wetlands · Stormwater · Nutrient removal'),
 ('carbon','Soil Health, Carbon Cycling, and Greenhouse Gases','How do water levels and soil management affect carbon storage and greenhouse gas emissions?','Soil organic matter · Emissions · Agricultural soils'),
 ('monitoring','Environmental Monitoring and Sensing','How can field sensors and aerial surveys reveal changes that individual samples miss?','Field sensors · Remote sensing · Environmental monitoring')]
scale_photos = [
 ('home-water-samples', 1600, 998, 'Rows of labeled glass bottles holding water samples'),
 ('home-treatment-columns', 1200, 1600, 'Six treatment columns with blue buckets and tubing'),
 ('home-outdoor-mesocosms', 1600, 994, 'Rows of blue outdoor mesocosms with plants and tubing'),
 ('home-wetland-sampling', 1411, 1600, 'A researcher in waders holding a sampling tube among wetland plants'),
]
def photo_carousel(photos, label):
 scale_slides = ''.join(
  f'<figure class="scale-slide"{" hidden" if index else ""}><img src="assets/{photo}.webp" width="{width}" height="{height}" alt="{E(alt)}" loading="lazy" decoding="async"></figure>'
  for index, (photo, width, height, alt) in enumerate(photos)
 )
 return carousel_markup(scale_slides, len(photos), label)

def carousel_markup(slides, count, label, autoplay=True):
 return f'''<div class="scale-carousel" role="group" aria-label="{E(label)}"{'' if autoplay else ' data-manual'}>
 <div class="scale-slides" aria-live="polite">{slides}</div>
 <div class="scale-controls" hidden>
  <button type="button" data-step="-1">Previous</button>
  <div class="scale-playback"><span class="scale-position" aria-hidden="true">1 / {count}</span><button type="button" class="scale-toggle">Pause</button></div>
  <button type="button" data-step="1">Next</button>
 </div>
</div><script src="scale-carousel.js" defer></script>'''
scale_carousel = photo_carousel(scale_photos, "Research across scales photographs")
body=f'''<section class="hero" style="--hero:url('{hero}')"><div class="wrap hero-content"><p class="eyebrow">THE HU RESEARCH GROUP</p><h1>Engineering biogeochemistry.<br><em>Advancing environmental quality.</em></h1><p>We study how carbon, nutrients, and emerging contaminants move through soils and water. Our lab experiments, field studies, and pilot-scale treatment systems help us design nature-based solutions for cleaner water, healthier soils, and more resilient ecosystems.</p><div class="button-row"><a class="button light" href="research.html">Explore our research</a><a class="button glass" href="people.html">Meet the lab</a></div></div><div class="hero-caption">{credit}</div></section><div class="opening-strip"><div class="wrap"><span class="strip-label">JOIN OUR LAB</span><a href="phd.html">Fully funded PhD · Fall 2027</a><span class="divider"></span><a href="postdoc.html">Postdoctoral scholar · Spring 2027</a><a class="strip-all" href="opportunities.html">View opportunities</a></div></div><section class="section pale"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">WHAT WE STUDY</p><h2>Research areas</h2></div><a class="text-link" href="research.html">Explore our approach</a></div><div class="research-grid">'''
for id,title,desc,tags in research:body+=f'<a class="research-card" href="research.html#{id}"><span class="research-icon icon-{id}" aria-hidden="true">'+({'water':'≈','wetlands':'≋','carbon':'◉','monitoring':'⌖'}[id])+f'</span><h3>{title}</h3><p>{desc}</p><span class="tags">{tags}</span></a>'
body+=f'''</div></div></section><section class="section"><div class="wrap field-grid">{scale_carousel}<div><p class="eyebrow">RESEARCH ACROSS SCALES</p><h2>From the lab to the field</h2><p>Understanding environmental systems starts with close observation. We connect the chemistry and biology of soils and waters to the performance of real-world management and treatment approaches.</p><p>Our work spans wetlands, cropping systems, and waste treatment systems, with a shared focus on carbon, nutrients, and environmental quality.</p><a class="text-link" href="research.html">Discover our research</a></div></div></section>{home_news}<section class="section pale"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">OUR WORK IN PRINT</p><h2>Research publications.</h2></div><a class="text-link" href="publications.html">Browse all publications</a></div><div id="recent-publications" class="recent-grid"></div></div></section>'''+cta()
page('index.html','Home',body)
# Research: grounded in the four existing research focal areas.
details={
 'water':('We follow nitrogen and phosphorus as they move through soils, sediments, and surface waters. By distinguishing nutrient forms, we can ask how much is available to microbes and how much may travel downstream.',['Dissolved organic nitrogen and its biodegradable fraction','Microbial nitrogen transformations, including denitrification','Nutrient exchange between soils and water']),
 'wetlands':('We use field studies and pilot systems to test how wetland design and operation affect water treatment. We examine how water moves through vegetation, soils, and treatment media, and how that contact changes nutrient removal.',['Constructed wetlands for watershed restoration','Vegetation, flow paths, and hydraulic loading','Stormwater treatment and nutrient removal']),
 'carbon':('We study what makes organic carbon persist in agricultural and wetland soils. We also measure greenhouse gases to understand how flooding, drainage, and soil amendments affect the balance between carbon storage and emissions.',['Soil organic matter and mineral-associated carbon','Soil health in managed agricultural systems','Carbon dioxide, methane, and nitrous oxide emissions']),
 'monitoring':('We combine field measurements with observations from satellites, drones, and ground vehicles. These tools connect what we measure at a sampling point with patterns across a wetland or agricultural field.',['Field sampling and environmental sensors','Satellite mapping of aquatic vegetation','Spatial and seasonal patterns in environmental conditions'])}
# The photographs are grouped by field activity; the names also identify their full-size links.
field_photos={
 'water':[
  ('nutrient-water-samples', 'Rows of capped glass bottles containing water samples', 2048, 1278),
  ('nutrient-shoreline', 'Two researchers working beside a body of water', 1200, 1600),
  ('nutrient-core', 'Layered wetland soil and water in a clear sampling tube', 1200, 1600),
  ('nutrient-mesocosms', 'Rows of blue outdoor mesocosms connected to pumps and tubing', 1200, 1600),
  ('nutrient-columns', 'Six laboratory columns connected to buckets and tubing', 1200, 1600)],
 'wetlands':[
  ('wetland-landscape', 'Clouds and marsh vegetation reflected in open water', 2048, 1536),
  ('wetland-sampling', 'Researcher in waders holding a long sampling tube among wetland plants', 1536, 2048),
  ('wetland-third', 'Floating leaves on the water surface in front of tall marsh plants', 1536, 2048)],
 'carbon':[
  ('soil-field', 'Field team working at several points in a cultivated field, with a white umbrella shading a tablet', 2048, 1536),
  ('soil-crop-fieldwork', 'Four researchers working among rows of plants in a sunny field', 1536, 2048),
  ('soil-sampling', 'Researchers collecting vegetation from a square sampling frame into a mesh bag', 1536, 2048),
  ('soil-corn', 'Two researchers looking at a laptop between rows of tall corn', 1080, 1440),
  ('soil-chamber', 'White soil gas chamber and tubing beneath a canopy of leaves', 1536, 2048),
  ('soil-mesocosm', 'Grass growing around a foil-covered chamber in a blue experimental container', 1536, 2048)],
 'monitoring':[
  ('monitoring-drone-flight', 'Research drone flying low over crop rows in a field', 2048, 1536),
  ('monitoring-drone-field', 'Researchers with a drone, controller, and laptop in a harvested field', 2048, 1536),
  ('monitoring-field-sensors', 'Pole-mounted monitoring instruments above a crop canopy', 1536, 2048),
 ],
}
def field_figure(photo):
 name,alt,w,h=photo
 src=f'assets/{name}.webp'
 if name in ('wetland-landscape','soil-field','nutrient-water-samples','monitoring-drone-flight'):
  sizes='(max-width: 700px) 95vw, (max-width: 1380px) 47vw, 620px'
 elif name.startswith('monitoring-'):
  sizes='(max-width: 700px) 95vw, (max-width: 1380px) 63vw, 810px' if name=='monitoring-drone-field' else '(max-width: 700px) 95vw, (max-width: 1380px) 36vw, 450px'
 elif name.startswith('wetland-'):
  sizes='(max-width: 440px) 95vw, (max-width: 700px) 46vw, (max-width: 1380px) 26vw, 330px'
 else:
  sizes='(max-width: 440px) 95vw, (max-width: 900px) 46vw, (max-width: 1380px) 24vw, 300px'
 return f'<figure class="field-photo"><a href="{src}" aria-label="View full photograph: {E(alt)}"><img src="{src}" srcset="assets/{name}-720.webp 720w, {src} {w}w" sizes="{sizes}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{E(alt)}"></a></figure>'
publications = json.loads((D/'publications.json').read_text())
def research_publications(area):
 entries = [paper for paper in publications if area in paper.get('research_areas', [])]
 items = []
 for paper in entries:
  url = paper['url'] or f'publications.html?area={area}&q={quote(paper["title"])}'
  items.append(f'<li><a href="{E(url)}">{E(paper["title"])}</a> <span>({E(paper["year"])})</span></li>')
 return f'<details class="research-publications"><summary>Related publications and data ({len(entries)})</summary><ul>{"".join(items)}</ul><a class="text-link" href="publications.html?area={area}">Browse this area on the Publications page</a></details>'

body=intro('RESEARCH','Engineering biogeochemistry','We study how water, microbes, and minerals shape the fate of nutrients and carbon, and use that knowledge to design and evaluate nature-based solutions.')+'<div class="wrap research-jumps">'+''.join(link('#'+r[0],E(r[1])) for r in research)+'</div><div class="wrap">'
for id,title,question,tags in research:
 desc,bullets=details[id]
 related=research_publications(id)
 heading=f'<p class="eyebrow">RESEARCH FOCUS</p><h2>{E(title)}</h2><p>{E(desc)}</p>'
 methods='<ul class="clean-list">'+''.join('<li>'+E(b)+'</li>' for b in bullets)+'</ul>'
 figures=[field_figure(photo) for photo in field_photos[id]]
 if id=='carbon':
  body+='<span id="climate"></span>'
 if id in ('carbon','water','monitoring'):
  overview=f'<div>{heading}{methods}</div>'+figures.pop(0)
 else:
  overview=f'<div>{heading}</div><div>{methods}</div>'
 body+=f'<section class="research-detail field-gallery-section" id="{id}">{overview}<div class="field-gallery-strip">{"".join(figures)}</div>{related}</section>'
body+='</div>'+cta();page('research.html','Research',body)
# People: names and research interests from the current public site.
grads=[('Zihan Li','M.S. student','Fall 2022','Soil greenhouse gas emissions; cover crops; soil carbon sequestration',3),('Shazneen Chowdhury','Ph.D. student','Fall 2024','Treatment wetlands; nutrient management under varying weather conditions; advanced water and wastewater treatment',4),('Ashish Bhatta','Ph.D. student','Fall 2025','Constructed wetlands; nutrient removal; real-time monitoring; wetland performance modeling',5),('SM Nahian Al Wasi','Ph.D. student','Fall 2025','Soil carbon sequestration; greenhouse gas emissions; large-scale treatment wetlands',6),('Camilla Guimaraes','M.S. student','Spring 2026','Water treatment; nutrient recovery; treatment wetlands',7)]
grads.append(('Md. Rashedul Haque','Ph.D. student','Fall 2026','Biogeochemistry; greenhouse gases; nanobubbles; ecotoxicology; transport and fate of pollutants','rashedul-haque'))
ugs=[
 ('Jacob Smith', 9, 'Spring 2025'),
 ('Abigail Itty', 11, 'Fall 2025'),
 ('Payton Estrada', 12, 'Fall 2025'),
 ('Kaylee Nguyen', 13, 'Fall 2025'),
 ('John Williams', 14, 'Fall 2025'),
 ('Javier Acosta-Aviles', 15, 'Fall 2025'),
 ('Jessa Carter', 17, 'Spring 2026'),
 ('Leah Johnson', 18, 'Spring 2026'),
 ('Khang Nguyen Vu', 19, 'Spring 2026'),
 ('Adrian Castaneda', None, 'Summer 2026'),
 ('Gavin Molina-Trupiano', None, 'Fall 2026'),
 ('Anahy Gonzalez-Mata', None, 'Fall 2026'),
 ('Diego Guerra', None, 'Fall 2026'),
 ('Herbert Sainvil', None, 'Fall 2026'),
 ('Dominic Segina', None, 'Fall 2026'),
 ('Zanielle Wells', None, 'Fall 2026'),
]
former_undergrads=[
 ('Parmeeda Mehrparvar', '2025–2026'),
 ('Madison Perunko', '2025–2026'),
 ('Tobias Seid', '2025–2026'),
 ('Aadi Sonawane', '2026'),
 ('Olivia Carmichael', '2025–2026'),
 ('Logan Spears', '2025–2026'),
 ('Quint Jamieson', '2025'),
 ('Ralph Rodriguez-Caraballo', '2025'),
 ('Mackenzie Hall', '2024'),
 ('Leah Hammons', '2022–2023'),
]
# Explicit byline matches avoid assigning papers to namesakes with the same initials.
lab_articles={p['url']:p for p in publications if p.get('url')}
student_papers={}
for work in json.loads((ROOT/'student-publications.json').read_text()):
 paper=lab_articles.get(work['url'])
 if paper is None:continue  # Only list publications in the lab bibliography.
 for name in work['students']:
  student_papers.setdefault(name,[]).append(paper)
def profile_id(name):return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
def publications_for(name):
 papers=sorted(student_papers.get(name,[]),key=lambda p:(-int(p['year']),p['title'].casefold()))
 if not papers:return ''
 items=''.join(f'<li><a href="{E(p["url"])}">{E(p["title"])}</a><span>{E(p["journal"])} · {E(str(p.get("date_label",p["year"])))}</span></li>' for p in papers)
 return f'<details class="student-papers"><summary>Lab publications ({len(papers)})</summary><ul aria-label="Publications by {E(name)}">{items}</ul></details>'
student_awards = {
 'Shazneen Chowdhury': ['UCF FCI Student Scholarship', 'Florida AWMA Scholarship'],
 'Zihan Li': ['Second Place, Graduate Student Poster Presentation, ASA–CSSA–SSSA Annual Meeting'],
 'Abigail Itty': ['EXCEL/COMPASS Summer Research Funding'],
 'Jacob Smith': ['WateReuse Florida Scholarship', 'UCF-OR Travel Award for the 2026 Florida Undergraduate Research Conference', 'UCF-OR Summer Undergraduate Research Fellowship', '2026 Florida Section AWWA Roy Likins Scholarship'],
 'Mackenzie Hall': ['UCF-OR Summer Undergraduate Research Fellowship'],
 'Leah Hammons': ['CALS/MAFES Undergraduate Research Scholars Program', 'MSU ORED Undergraduate Research Program'],
}
def awards_for(name):
 items = student_awards.get(name)
 if not items:
  return ''
 entries = ''.join(f'<li>{E(award)}</li>' for award in items)
 return f'<div class="student-awards"><strong>Awards</strong><ul>{entries}</ul></div>'
def portrait(name,i):
 named_photo = A/f'portrait-{profile_id(name)}.webp'
 if named_photo.exists():
  return f'<div class="profile-photo-frame"><img class="profile-headshot" src="assets/{named_photo.name}" alt="{E(name)}" loading="lazy"></div>'
 # Source image 20 is a branded placeholder rather than a portrait.
 framed = 'wasi-headshot-outdoors.webp' if i==6 else f'profile-{i}.webp'
 original = 'wasi-portrait-outdoors.jpg' if i==6 else f'people-{i}.jpg'
 if i!=20 and (A/original).exists():
  source = framed if (A/framed).exists() else original
  img = f'<img class="profile-headshot" src="assets/{source}" alt="{E(name)}" loading="lazy">'
  if i==6:
   return f'<a class="profile-headshot-link" href="assets/{original}" aria-label="Open full-resolution portrait of {E(name)}">{img}</a>'
  return img
 return '<img class="profile-headshot profile-placeholder" src="assets/engineering-biogeochemistry-placeholder.webp" alt="Engineering Biogeochemistry Lab student photo placeholder" loading="lazy">'
body=intro('PEOPLE','The people behind the science.','A research community connecting environmental engineering, soil and water sciences, and biogeochemistry.')
group_photos = [
 ('group-fall-2026', 2048, 1536, 'Lab members posing together outside a campus building'),
 ('group-waterfront', 1800, 1350, 'Six members of the research team posing together outdoors near the water'),
 ('group-fieldwork', 1800, 1616, 'Five members of the research team taking a group photo in field gear'),
 ('group-selfie', 1350, 1800, 'Three members of the research team taking a low-angle selfie in field gear'),
 ('group-field-trip-2022', 1536, 2048, 'Four people posing by a pickup truck in a grassy field'),
 ('group-fieldwork-tailgate', 1080, 1440, 'Two people in sun hats sitting on a pickup truck tailgate'),
 ('group-poster-session', 2048, 1536, 'Four lab members posing in front of a UCF research poster'),
]
def group_photo(photo):
 name, width, height, alt = photo
 src = f'assets/{name}.webp'
 return f'<figure class="field-photo"><a href="{src}" aria-label="Open full photo: {E(alt)}"><img src="{src}" width="{width}" height="{height}" alt="{E(alt)}" loading="lazy" decoding="async"></a></figure>'

group_slides = (
 f'<div class="scale-slide">{group_photo(group_photos[0])}</div>',
 f'<div class="scale-slide" hidden>{group_photo(group_photos[1])}</div>',
 f'<div class="scale-slide group-photo-pair" hidden>{group_photo(group_photos[2])}{group_photo(group_photos[3])}</div>',
 f'<div class="scale-slide group-photo-pair" style="grid-template-columns: repeat(2, minmax(0, 1fr))" hidden>{group_photo(group_photos[4])}{group_photo(group_photos[5])}</div>',
 f'<div class="scale-slide" hidden>{group_photo(group_photos[6])}</div>',
)
body+=f'<section class="section people-group-photos" id="group-photos"><div class="wrap"><h2>Group photos</h2>{carousel_markup("".join(group_slides), len(group_slides), "Lab group photos", autoplay=False)}</div></section>'
people_groups=[('pi','PI'),('current-member','Current Member'),('alumni','Alumni')]
body+='<nav class="people-tabs" aria-label="People categories"><div class="wrap" data-people-tabs>'+''.join(f'<a id="tab-{slug}" href="#{slug}">{label}</a>' for slug,label in people_groups)+'</div></nav>'
body+='<div class="people-panel" id="pi">'
body+=f'<section class="section" id="jing-hu"><div class="wrap pi-grid"><div class="pi-photo">{portrait("Jing Hu",2)}</div><div><p class="eyebrow">PRINCIPAL INVESTIGATOR</p><h2>Jing Hu, Ph.D.</h2><p class="pi-role">Assistant Professor · University of Central Florida</p><p>Department of Civil, Environmental, and Construction Engineering</p><h3>Research profile</h3><p>Dr. Jing Hu is an environmental engineer whose research advances engineering biogeochemistry to understand, design, and optimize nature-based solutions for improving water quality and ecosystem resilience. By integrating biogeochemistry, hydrology, microbial ecology, and ecological engineering, her research reveals the mechanisms governing nutrient cycling and translates these discoveries into innovative technologies for sustainable water management. Her work bridges fundamental science with engineering implementation to address challenges in watershed restoration, stormwater treatment, agricultural sustainability, and climate resilience.</p><h3>Education</h3><ul class="education"><li><b>Ph.D., Soil and Water Sciences</b><span>University of Florida</span></li><li><b>M.S. & B.S., Agricultural and Biosystems Engineering</b><span>China Agricultural University</span></li></ul><div class="button-row"><a class="button dark" href="mailto:jing.hu@ucf.edu">Contact Jing</a><a class="text-link" href="{scholar}" target="_blank" rel="noopener">Google Scholar</a><a class="text-link" href="https://www.linkedin.com/in/jing-hu-68379246/" target="_blank" rel="noopener">LinkedIn</a></div></div></div></section>'
body+='</div><div class="people-panel" id="current-member"><span id="current-students" class="people-anchor" aria-hidden="true"></span>'
for degree,heading,slug in [('Ph.D. student','Ph.D. Students','phd-students'),('M.S. student','M.S. Students','ms-students')]:
 body+=f'<section class="section pale" id="{slug}"><div class="wrap"><h2>{heading}</h2><div class="people-grid">'
 for n,role,since,desc,i in grads:
  if role!=degree:continue
  urls=[]
  if n=='Zihan Li':
   urls=[('Google Scholar','https://scholar.google.com/citations?hl=en&user=3NV83-8AAAAJ')]
  elif n=='SM Nahian Al Wasi':
   urls=[('Google Scholar','https://scholar.google.com/citations?user=DW2F5K8AAAAJ&hl=en'),('LinkedIn','https://www.linkedin.com/in/sm-nahian-al-wasi')]
  elif n=='Shazneen Chowdhury':
   urls=[('Google Scholar','https://scholar.google.com/citations?user=9opd8R4AAAAJ&hl=en&oi=ao'),('LinkedIn','https://www.linkedin.com/in/shazneenchowdhury/')]
  elif i=='rashedul-haque':
   urls=[('Google Scholar','https://scholar.google.com/citations?user=23LgOdMAAAAJ&hl=en'),('LinkedIn','https://www.linkedin.com/in/md-rashedul-haque-39591a195/'),('ORCID','https://orcid.org/0000-0003-4225-428X')]
  extra='<p class="profile-links">'+ ' · '.join(f'<a href="{E(url)}" target="_blank" rel="noopener">{label}</a>' for label,url in urls)+'</p>' if urls else ''
  anchor=f' id="{profile_id(n)}"'
  body+=f'<article class="person"{anchor}>{portrait(n,i)}<h3>{n}</h3><p class="person-role">{role} · Since {since}</p><p>{desc}</p>{extra}{awards_for(n)}{publications_for(n)}</article>'
 body+='</div></div></section>'

body+='<section class="section"><div class="wrap"><h2>Undergraduate researchers.</h2><div class="undergrad-grid">'
for n,i,since in ugs:body+=f'<article class="person" id="{profile_id(n)}">{portrait(n,i)}<h3>{n}</h3><p class="person-role">Since {E(since)}</p>{awards_for(n)}{publications_for(n)}</article>'
body+='</div></div></section></div><div class="people-panel" id="alumni"><section class="section pale"><div class="wrap alumni"><div><p class="eyebrow">OUR EXTENDED COMMUNITY</p><h2>Lab alumni.</h2></div><div><h3>Postdoctoral associate</h3><p>Nisarga Kodadinne Narayana · 2023</p><h3>Undergraduate research assistants</h3><ul class="alumni-roster">' + ''.join(f'<li id="{profile_id(name)}">{E(name)} · {E(years)}{awards_for(name)}{publications_for(name)}</li>' for name,years in former_undergrads) + '</ul></div></div></section>'
body+='</div><script src="people-tabs.js" defer></script>'
page('people.html','People',body)
area_options = ''.join(f'<option value="{area}">{E(title)}</option>' for area,title,*_ in research)
body=intro('PUBLICATIONS','Science to share.','Browse journal articles, other publications, and public data from our work on water, soil, and climate.')+f'<section class="section pub-section"><div class="wrap"><div class="research-jumps pub-jumps"><a href="#journal-articles">Journal Articles</a><a href="#other-publications">Other Publications</a><a href="#public-dataset">Public Dataset</a></div><div class="pub-toolbar"><label class="search-label"><span>Search publications</span><input id="pub-search" type="search" placeholder="Search titles, authors, journals…"></label><label><span>Research area</span><select id="pub-area"><option value="">All research areas</option>{area_options}</select></label><label><span>Year</span><select id="pub-year"><option value="">All years</option></select></label></div><div class="pub-meta"><span id="pub-count" role="status" aria-live="polite">Loading publications…</span><a class="text-link" href="{scholar}" target="_blank" rel="noopener">View Google Scholar</a></div><p class="student-note">** Graduate student · * Undergraduate student under Jing Hu’s direct supervision</p><div id="publication-list"></div><noscript><p>Enable JavaScript to search and display the publication list, or visit <a href="{scholar}">Google Scholar</a>.</p></noscript></div></section>'
page('publications.html','Publications',body)
body=intro('TEACHING','Learning to engineer<br>a healthier environment.','Building the foundations to understand environmental systems and solve practical engineering problems.')+'''<section class="section"><div class="wrap course-grid"><div class="course-code">ENV<br><strong>3001</strong><span>UNDERGRADUATE · 3 CREDITS</span></div><div><p class="eyebrow">UCF · CIVIL, ENVIRONMENTAL, AND CONSTRUCTION ENGINEERING</p><h2>Introduction to<br>Environmental Engineering</h2><p>A core undergraduate course introducing environmental engineering practice, the chemistry of environmental systems, and tools for evaluating and designing treatment processes.</p><h3>What students learn</h3><ul class="clean-list"><li>Explore environmental engineering careers, professionalism, and ethics.</li><li>Apply environmental chemistry to engineering problems.</li><li>Conduct mass and energy balances for reactors and natural systems, along with chemical and thermodynamic calculations.</li><li>Use engineering tools to address water and wastewater treatment, solid waste disposal, and air pollution.</li></ul><a class="button dark" href="mailto:jing.hu@ucf.edu?subject=Course%20inquiry">Ask about the course</a></div></div></section><section class="section pale"><div class="wrap intro-grid"><p class="eyebrow">LEARNING THROUGH RESEARCH</p><div><h2>Questions become discoveries.</h2><p class="large-text">Our lab connects fieldwork, experimental methods, and data analysis to environmental challenges.</p><a class="text-link" href="opportunities.html">Explore research opportunities</a></div></div></section>'''
page('teaching.html','Teaching',body)
body=intro('JOIN OUR LAB','Curious minds.<br>Meaningful research.','We welcome motivated researchers interested in environmental biogeochemistry, water quality, soil health, and nature-based solutions.')+'''<section class="section"><div class="wrap"><div class="section-heading"><h2>Current opportunities.</h2><span class="muted">2027 recruitment</span></div><div class="jobs-grid"><article class="job-card"><span class="job-tag">FULLY FUNDED · FALL 2027</span><h3>Ph.D. researcher</h3><p>Conduct field and laboratory research in soil and water biogeochemistry across natural and engineered systems.</p><a class="button dark" href="phd.html">View PhD position</a></article><article class="job-card"><span class="job-tag">SPRING 2027</span><h3>Postdoctoral scholar</h3><p>Lead laboratory and outdoor pilot experiments focused on nitrogen transformation, removal, and water treatment.</p><a class="button dark" href="postdoc.html">View postdoc position</a></article></div><div class="undergrad-note"><h3>Undergraduate research</h3><p>No undergraduate positions are currently available. Please reach out in Spring 2027 to inquire about future opportunities.</p><a class="text-link" href="mailto:jing.hu@ucf.edu?subject=Undergraduate%20research%20inquiry">Contact Jing Hu</a></div></div></section>'''
page('opportunities.html','Join us',body)
# Preserve the requirements and application materials from each original advertisement.
jobs={
'phd':('Ph.D. researcher','Fully funded · Fall 2027','Conduct field and laboratory research in soil and water biogeochemistry across natural and engineered soil and aquatic systems.',[
('Your research',['Field sampling and laboratory analysis of soil, water, and gas samples.','Data management, statistical analysis, and reproducible analytical workflows.','Peer-reviewed publications and conference presentations.']),('Required qualifications',['A master’s degree in Environmental Engineering, Environmental Science, Soil Science, Water Science, Biology, Chemistry, or a closely related discipline, completed by enrollment.','Strong written and oral communication skills.','A professional, collaborative working style.']),('Preferred qualifications',['Research experience with soils, wetlands, cropping systems, or stormwater treatment systems.','Demonstrated analytical laboratory skills.','Training or experience in statistics; proficiency in R or Python.','A valid driver’s license and ability to drive for fieldwork.']),('Funding',['Full funding is available for competitive applicants through a combination of fellowship and graduate assistantship support.'])],['Curriculum vitae (CV).','Statement of research interests (1–2 pages).','Unofficial transcripts.','Contact information for two to three references.'],'PhD27'),
'postdoc':('Postdoctoral scholar','Spring 2027','Lead laboratory and outdoor pilot experiments investigating nitrogen transformation and removal in treatment systems.',[
('Your role',['Experimental design, system operation, and water quality monitoring.','Data analysis, manuscript and proposal preparation.','Student mentoring.']),('Required qualifications',['Ph.D. in Environmental Engineering, Environmental Science, Soil and Water Sciences, Biogeochemistry, or a closely related field.','Experience in nitrogen cycling, organic matter dynamics, or water treatment processes.','Strong laboratory, experimental design, quantitative analysis, and scientific writing skills.','A valid U.S. driver’s license, ability to drive, and willingness to travel frequently to the study site.']),('Preferred experience',['Nutrient analyses for soil and water samples.','Column, mesocosm, or pilot-scale treatment experiments.','Hydraulics, flow control, residence time, and treatment performance evaluation.','Analytical instrument operation, troubleshooting, and laboratory QA/QC.','Statistical analysis using R, Python, or similar software.'])],['Cover letter describing relevant experience and research interests.','Curriculum vitae (CV).','Two representative first-author publications.','Contact information for three references.'],'Postdoctoral Application')}
from urllib.parse import quote
for slug,(title,start,desc,sections,materials,subject) in jobs.items():
 body=intro('RESEARCH OPPORTUNITY',title,desc)+f'<section class="section"><div class="wrap job-layout"><article><a class="text-link back-link" href="opportunities.html">All opportunities</a><span class="job-tag">{start.upper()}</span>'
 for h,items in sections:body+='<h2 class="job-section-title">'+h+'</h2><ul class="clean-list">'+''.join('<li>'+s+'</li>' for s in items)+'</ul>'
 body+=f'</article><aside class="apply-panel"><p class="eyebrow">HOW TO APPLY</p><h2>Let’s hear from you.</h2><p>Email Dr. Jing Hu with the subject line <strong>{subject}</strong> and include:</p><ul>'+''.join('<li>'+m+'</li>' for m in materials)+f'</ul><a class="button dark" href="mailto:jing.hu@ucf.edu?subject={quote(subject)}">Email your application</a><a href="mailto:jing.hu@ucf.edu">jing.hu@ucf.edu</a></aside></div></section>'
 page(slug+'.html',title,body)
body=intro('CONTACT','Let’s connect.','For research collaborations, prospective student inquiries, and questions about our work.')+'''<section class="section"><div class="wrap contact-grid"><div><p class="eyebrow">PRINCIPAL INVESTIGATOR</p><h2>Jing Hu, Ph.D.</h2><p>Assistant Professor<br>Department of Civil, Environmental, and Construction Engineering<br>University of Central Florida</p><a class="email-large" href="mailto:jing.hu@ucf.edu">jing.hu@ucf.edu</a><h3>Mailing address</h3><p>12800 Pegasus Dr<br>Orlando, FL 32816</p><a class="text-link" href="https://www.google.com/maps/search/?api=1&query=12800+Pegasus+Dr+Orlando+FL+32816" target="_blank" rel="noopener">View campus location</a></div><div class="contact-panel"><span class="ucf-word">UCF</span><p class="eyebrow">ORLANDO, FLORIDA</p><h2>Engineering<br>Biogeochemistry Lab</h2><p>Connecting environmental engineering<br>with the science of living systems.</p><a class="button light" href="opportunities.html">Join our research community</a></div></div></section>'''
page('contact.html','Contact',body)
resources=[
 ('UCF and CECE',[
 ('University of Central Florida','University','Explore UCF’s academic programs, campus life, and visitor information.','https://www.ucf.edu/'),
 ('Civil, Environmental and Construction Engineering (CECE)','Department','Meet the faculty, explore research areas, and find contacts in the lab’s home department.','https://www.cece.ucf.edu/')]),
 ('Graduate admissions',[
 ('Environmental Engineering Ph.D.','Doctoral program','Explore research areas, degree requirements, and admission criteria for the doctorate.','https://www.cece.ucf.edu/ph-d-in-environmental-engineering/'),
 ('Environmental Engineering master’s programs','Master’s programs','Compare the two degree paths and review thesis and nonthesis options.','https://www.cece.ucf.edu/master-of-science-in-environmental-engineering/'),
 ('Application deadlines and requirements','Before you apply','Look up your program and entry term to find the deadline and required application materials.','https://graduate.ucf.edu/application-deadlines-and-requirements/'),
 ('Guidance for international applicants','International admissions','Check UCF’s instructions for international transcripts and English proficiency.','https://graduate.ucf.edu/international-applicants/'),
 ('Start or resume your application','UCF graduate application','Create an account or sign in to complete your graduate application.','https://applynow.graduate.ucf.edu/apply/')]),
 ('Research affiliations',[
 ('Renewable Energy and Chemical Transformation (REACT)','UCF faculty research cluster','Explore projects on catalysts for renewable fuels and chemical processes, along with the researchers behind them.','https://www.ucf.edu/research/energy-conversion-propulsion/'),
 ('UCF Coastal: Center for Integrated Coastal Research','UCF research center','Meet researchers studying how coasts change and how communities can manage coastal resources and flood risk.','https://www.ucf.edu/research/sustainable-coastal-systems/')]),
 ('For UCF students',[
 ('UCF Libraries','Literature searches','Find journal articles, subject databases, and research guides when starting a literature review.','https://library.ucf.edu/'),
 ('Undergraduate Research','Getting started at UCF','Explore ways to find a mentor, earn course credit, or apply for a student research grant.','https://academicsuccess.ucf.edu/our/')])]
def resource_id(heading): return re.sub(r'[^a-z0-9]+','-',heading.lower()).strip('-')
resource_body=intro('STUDY & RESEARCH','Resources','Explore UCF and CECE, find graduate application guidance, and discover research opportunities and resources for students.')
resource_body+='<nav aria-label="Resource topics" class="resource-topics"><div class="wrap">'+''.join(f'<a href="#{resource_id(heading)}">{E(heading)}</a>' for heading,_ in resources)+'</div></nav>'
for idx,(heading,items) in enumerate(resources):
 resource_body+=f'<section id="{resource_id(heading)}" class="resource-section section'+(' pale' if idx%2 else '')+'"><div class="wrap intro-grid"><h2>'+E(heading)+'</h2><div class="news-stories">'
 for title,org,desc,url in items:
  resource_body+=f'<article><p class="eyebrow">{E(org)}</p><h3><a class="text-link" href="{E(url)}">{E(title)}</a></h3><p>{E(desc)}</p></article>'
 resource_body+='</div></div></section>'
page('resources.html','Resources',resource_body)
print('Built',len(list(D.glob('*.html'))),'pages')
