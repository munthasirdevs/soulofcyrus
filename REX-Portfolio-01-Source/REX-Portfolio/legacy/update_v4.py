from pathlib import Path
import json,shutil
R=Path(__file__).parent/'dist';D=json.loads((R/'content.json').read_text());P={p['id']:p for p in D['projects']}
def cp(src,sub):
 out=R/'assets'/sub;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out);return '/'+str(out.relative_to(R))
F=json.load(open('/workspace/shared/rex-v4-feedback/manifest.json'))
for t in F['thumbnails']:
 p=P[t['project']]
 if t.get('type')=='video':p['thumbnail']=next(a.copy() for a in p['media'] if a['type']=='video')
 else:p['thumbnail']={'type':'image','src':cp(t['output'],'thumbnails/'+Path(t['output']).name),'alt':p['title']+' selected thumbnail'}
D['portrait']=cp(F['portrait']['output'],'portrait/cyrus-rex-extended.webp')
M=json.load(open('/workspace/shared/rex-v4-new-media/manifest.json'));groups={}
credits=['Katherine Chase','Matthew McBrayer','Vino Li','Zach Inglis']
for a in M['assets']:
 g=a['group'];d={'type':'image','src':cp(a['web'],g+'/'+Path(a['web']).name),'alt':a['alt'],'width':a['width'],'height':a['height'],'source_id':a['library_file_id']}
 if g=='photography' and a['group_index']<=4:d['caption']='Photo editing by Cyrus Rex. Original photograph: '+credits[a['group_index']-1]+' / Unsplash.'
 groups.setdefault(g,[]).append(d)
 if a.get('also_food_beverage') and not any(x.get('source_id')==d['source_id'] for x in P['food-beverage']['media']):P['food-beverage']['media'].append(d.copy())
print('groups',[(g,len(a)) for g,a in groups.items()])
f=P['food-beverage'];f['media']=[a for a in f['media'] if a.get('source_id')!='libfile_90a9ca5544c481919fae7e1d7bc006b1' and 'matcha-1' not in a['src'].lower() and 'matcha-motion.mp4' not in a['src']]
f['media'].append({'type':'video','src':cp('/workspace/shared/rex-v4-matcha/matcha-motion-web.mp4','projects/food-beverage/matcha-motion.mp4'),'poster':cp('/workspace/shared/rex-v4-matcha/matcha-poster.webp','projects/food-beverage/matcha-poster.webp'),'alt':'Matcha animated visual study','loop':True})
f['format']='Still imagery & short-form films'
sneaker=groups['sole-frequency']
p={'id':'sole-frequency','title':'SOLE FREQUENCY','category':'Sneaker visuals','headline':'SOLE FREQUENCY.','intro':'A collection of sneaker visuals exploring movement, shape and colour.','format':'Eight-image visual collection','focus':'Sneaker imagery / Composition','disciplines':['design'],'media':sneaker,'cover':sneaker[0],'color':'#181818'}
D['projects']=[P[x] for x in ['cambrook','lois-lip-oil','lois-sunscreen','designora-01','designora-02','lois-lipstick','travel-agencies','food-beverage','supportive-care']]+[p]
D['photography_albums']=[{'id':'selected-photography','title':'Photography / Selected','intro':'A gallery of photographs and photo-editing work. Original photographers are credited on the edited source images.','media':groups['photography']},{'id':'monochromatic-24','title':'MONOCHROMATIC/24','intro':'A monochromatic visual collection.','media':groups['monochromatic-24']}]
(R/'content.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
