from pathlib import Path
import json,shutil
R=Path(__file__).parent/'dist'; dest=R/'assets/projects';dest.mkdir(parents=True,exist_ok=True)
L=json.load(open('/workspace/shared/rex-v3-library/manifest.json'));B=json.load(open('/workspace/shared/rex-v3-lois/manifest.json'))
def copy(src,group,filename=None):
 src=Path(src);out=dest/group/(filename or src.name);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out);return '/'+str(out.relative_to(R))
def normal(a,group):
 src=a.get('webp_path') if a['type']=='image' else a['web_path'];src=src or a['web_path']
 wh=a.get('web_dimensions',[a.get('web_width',a.get('width')),a.get('web_height',a.get('height'))])
 d={'src':copy(src,group),'type':a['type'],'alt':a.get('alt', {'lip-oil':'LOIS lip-oil product composition','lipstick':'LOIS lipstick product visual','sunscreen':'LOIS sunscreen campaign visual','food-beverage':'Food and beverage film'}.get(group.split('/')[-1], 'LOIS lipstick collection visual')),'source_id':a.get('library_file_id',a.get('source_id'))}
 if wh[0]:d.update(width=wh[0],height=wh[1])
 if a.get('poster_path'):d['poster']=copy(a['poster_path'],group)
 return d
lib={}
for p in L['projects']:
 assets=[normal(a,p['slug']) for a in p['assets']];lib[p['slug']]=(p,assets)
groups={}
for a in B['assets']:
 g=a['group'];groups.setdefault(g,[]).append(normal(a,'lois/'+g))
projects=[]
def project(id,title,category,headline,intro,fmt,focus,discip,assets,cover=0,color='#191919',**extra):
 p={'id':id,'title':title,'category':category,'headline':headline,'intro':intro,'format':fmt,'focus':focus,'disciplines':discip,'media':assets,'cover':assets[cover].copy(),'color':color,**extra}
 if p['cover']['type']=='video':p['cover']={'type':'image','src':p['cover']['poster'],'alt':title+' film still'}
 projects.append(p)
def la(slug):return lib[slug][1]
# Keep the intake sequence as a reversible first pass, with Cambrook first.
c=la('cambrook'); cover=next(i for i,a in enumerate(c) if a['source_id']=='libfile_217fdd0e8b5481919a5425069dc083b0')
project('cambrook','Cambrook','Social media campaign','Extraordinary nuts. Everyday moments.','A social media campaign bringing Cambrook’s nut collection into product-led compositions, shared-table scenes and seasonal moments.','Social imagery & short-form motion','Product presentation / Social design',['design','film'],c,cover,'#303324',context='Founded in 2012, Cambrook produces baked, seasoned and caramelised nuts in Andover, Hampshire.',source='https://www.cambrookfoods.co.uk/about-us/')
project('designora-01','DESIGNORA / 01','Interior studio visuals','A new home, in focus.','A five-part visual series for DESIGNORA, bringing the living spaces of a home together through a consistent presentation.','Five-image social series','Layout / Typography / Interior imagery',['design'],la('designora-project-01'),0,'#b59033')
project('designora-02','DESIGNORA / 02','Interior studio visuals','One home. A complete picture.','A room-by-room visual presentation for DESIGNORA, moving from bedrooms and living spaces to the kitchen and finishing details.','Eight-image project presentation','Editorial sequence / Social design',['design'],la('designora-project-02'),5,'#bcb8af')
s=groups['sunscreen'];cover=next(i for i,a in enumerate(s) if a['source_id']=='libfile_e8e1e4d897a8819199a531723b7a309a')
project('lois-sunscreen','LOISCHLOE / Sunscreen','Beauty campaign','Under the sun.','A sunscreen campaign in a world of sunlit skin, pale sand and clean product compositions.','Eight campaign visuals','Beauty imagery / Product presentation',['design'],s,cover,'#dedbd0')
o=groups['lip-oil'];cover=next(i for i,a in enumerate(o) if a['type']=='image')
project('lois-lip-oil','LOIS / Lip Oil','Beauty imagery & film','A study in gloss.','Lip-oil imagery and a product film exploring reflective surfaces, close detail and the product’s visual character.','Five stills & one film','Product imagery / Moving image',['design','film'],o,cover,'#e7cec3')
k=groups['lipstick']+groups['lipstick/lois-1']+groups['lipstick/tangerine']+groups['lipstick/ruby-dance'];cover=next(i for i,a in enumerate(k) if a['source_id']=='1iN0aoQhfqkRY5c3aqJKmYVwpSUMUHNQi')
project('lois-lipstick','LOISCHLOE / Lipstick','Beauty imagery & film','Colour, with character.','A collection of lipstick visuals spanning product stills, colour-led compositions and moving image. French Love and Nude Classic open the story, followed by the supplied lipstick collections.','Seventeen stills & one film','Product detail / Colour / Moving image',['design','film'],k,cover,'#b99079')
project('travel-agencies','Travel Agencies','Travel campaign design','A destination in every frame.','A collection of destination-led travel designs for Bali, Dubai, Vietnam, Paris, Barcelona and Kerala.','Six travel visuals','Campaign layout / Destination imagery',['design'],la('travel-agencies'),0,'#86aaa9')
f=la('food-beverage')+groups['food-beverage'];cover=next(i for i,a in enumerate(f) if 'blue-berry' in a['src'])
project('food-beverage','FOOD & BEVERAGE','Visual design & motion','Made to stir the senses.','Drink-led visual studies and short-form films, from blueberry and matcha to espresso, mint and cocktail moments.','Five stills & three films','Food styling imagery / Typography / Motion',['design','film'],f,cover,'#baabd3')
project('supportive-care','Supportive Solutions','Brochure design','Care, clearly communicated.','A brochure presentation for Supportive Solutions Home Care, LLC. A consistent system of photography, information panels and lime-green accents carries through the spreads.','Four brochure mockups','Editorial layout / Print presentation',['design'],la('supportive-solution-care'),0,'#292d2f')
D={'portrait':'/assets/portrait/cyrus-rex.webp','aboutVideo':None,'instagram':'https://www.instagram.com/soulofcyrus/','whatsapp':'https://wa.me/8801938466771','projects':projects}
(R/'content.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
print('Projects:',len(projects),'Media:',sum(len(p['media']) for p in projects))
