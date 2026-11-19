import json,re,hashlib,collections,datetime
from pathlib import Path
from shapely.geometry import shape, box
from shapely.ops import transform
from pyproj import Transformer
p=Path(__file__).resolve().parents[1]
raw=json.loads((p/'source/公害陳情案件數.json').read_text(encoding='utf-8-sig')); rows=[];seen=set()
for r in raw:
 m=re.fullmatch(r'(\d+)年(?:\s*(\d+)月)?',r['item1']);assert m
 key=(int(m[1])+1911,int(m[2]) if m[2] else 0,r['item2']);assert key not in seen;seen.add(key)
 rows.append({'year':key[0],'month':key[1],'name':key[2],'odor':int(r['value3']),'all':int(r['value1'])})
checks=[]
for year,month in sorted({(x['year'],x['month']) for x in rows}):
 rr=[x for x in rows if x['year']==year and x['month']==month];assert len(rr)==23
 total=next(x for x in rr if x['name']=='總計');cc=[x for x in rr if x['name']!='總計'];assert sum(x['odor'] for x in cc)==total['odor'];assert sum(x['all'] for x in cc)==total['all'];checks.append([year,month])
for year in range(2022,2026):
 for name in {x['name'] for x in rows}:
  a=next(x for x in rows if x['year']==year and x['month']==0 and x['name']==name)
  mm=[x for x in rows if x['year']==year and x['month']>0 and x['name']==name];assert len(mm)==12
  assert sum(x['odor'] for x in mm)==a['odor']
land=json.load(open(p/'source/counties.geojson'));tr=Transformer.from_crs(4326,3826,always_xy=True).transform
geoms=[transform(tr,shape(f['geometry']).intersection(box(118,21.8,123,26.5))) for f in land['features']];bounds=[g.bounds for g in geoms];x0=min(b[0] for b in bounds);x1=max(b[2] for b in bounds);y0=min(b[1] for b in bounds);y1=max(b[3] for b in bounds);scale=min(650/(x1-x0),680/(y1-y0));ox=(700-(x1-x0)*scale)/2;oy=25
xy=lambda x,y:(round(ox+(x-x0)*scale,2),round(oy+(y1-y)*scale,2))
paths=[];anchors={}
for f,g in zip(land['features'],geoms):
 name=f['properties']['COUNTYNAME'];polys=list(g.geoms) if g.geom_type=='MultiPolygon' else [g];d=[]
 for poly in polys:
  for ring in [poly.exterior,*poly.interiors]:
   pts=[xy(x,y) for x,y in ring.coords];d.append('M'+'L'.join(f'{x},{y}' for x,y in pts)+'Z')
 anchor=max(polys,key=lambda q:q.area).representative_point();anchors[name]=xy(anchor.x,anchor.y)
 paths.append(f'<path data-name="{name}" d="{" ".join(d)}" tabindex="0" role="button" aria-label="{name}"/>')
qa={'downloaded_rows':len(rows),'unique_periods':len(checks),'counties_per_period':22,'national_reconciliation_all_periods':True,'annual_month_sum_2022_2025':True,'source_end':'2026-09','annual_default':2025,'national_2025_odor':67248,'national_2025_all':272191,'no_population_rate':True,'no_point_locations':True,'download_sha256':hashlib.sha256((p/'source/STAT_P_134_Resource.zip').read_bytes()).hexdigest()}
(p/'evidence/data-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(p/'data.json').write_text(json.dumps(rows,ensure_ascii=False))
template=(p/'scripts/template.html').read_text();template=template.replace('__PATHS__',''.join(paths)).replace('__DATA__',json.dumps(rows,ensure_ascii=False)).replace('__ANCHORS__',json.dumps(anchors,ensure_ascii=False));(p/'index.html').write_text(template)
print(json.dumps(qa,ensure_ascii=False,indent=2))
