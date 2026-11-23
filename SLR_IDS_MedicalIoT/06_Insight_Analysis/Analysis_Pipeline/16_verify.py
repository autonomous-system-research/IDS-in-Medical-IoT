import io
import csv, json, os, re
from collections import Counter
B='SLR_IDS_MedicalIoT'
def rd(p):
    with open(os.path.join(B,p),encoding='utf-8') as f: return list(csv.DictReader(f))
problems=[]; checks=[]
def ck(name, cond, detail=''):
    checks.append((name,'PASS' if cond else 'FAIL',detail))
    if not cond: problems.append(name+' :: '+detail)

ident=rd('02_Downloaded_Papers/01_identification_register_raw.csv')
dedup=rd('02_Downloaded_Papers/02_deduplicated_records.csv')
title=rd('03_Screening/01_title_screening.csv')
venue=rd('03_Screening/02_venue_eligibility_screening.csv')
abst =rd('03_Screening/03_abstract_screening.csv')
qa   =rd('03_Screening/04_quality_assessment_scores.csv')
fin  =rd('02_Downloaded_Papers/03_final_50_included_studies.csv')
bib  =rd('02_Downloaded_Papers/04_final_50_bibtex.csv')
ext  =rd('05_Data_Extraction/01_metadata_extraction_all50.csv')

ck('Identification register = 690 raw records', len(ident)==690, f'{len(ident)}')
ck('Deduplicated register = 594 unique records', len(dedup)==594, f'{len(dedup)}')
ck('Title screening covers every unique record', len(title)==594, f'{len(title)}')
ti=[r for r in title if r['decision']=='INCLUDE']
ck('Title screening includes = 242', len(ti)==242, f'{len(ti)}')
ck('Every title-screening row has a reason', all(r['reason_code_and_rationale'].strip() for r in title))
ck('Venue screening covers all title-includes', len(venue)==242, f'{len(venue)}')
vs=[r for r in venue if r['decision']=='SOUGHT FOR RETRIEVAL']
ck('Venue screening -> 153 sought for retrieval', len(vs)==153, f'{len(vs)}')
ck('Abstract screening covers all retrieved', len(abst)==153, f'{len(abst)}')
ai=[r for r in abst if r['decision']=='INCLUDE']
ck('Abstract screening includes = 112', len(ai)==112, f'{len(ai)}')
ck('Every abstract-screening row has a reason', all(r['reason_code_and_rationale'].strip() for r in abst))
ck('QA scored every abstract-include', len(qa)==112, f'{len(qa)}')
passed=[r for r in qa if r['passed_threshold']=='YES']
ck('QA >= 75 -> 83 studies', len(passed)==83, f'{len(passed)}')
ck('All QA totals equal the sum of their 10 item scores',
   all(sum(int(r[f'Q{i}_score']) for i in range(1,11))==int(r['total_score_out_of_100']) for r in qa))
ck('No QA item score outside 0-10',
   all(0<=int(r[f'Q{i}_score'])<=10 for r in qa for i in range(1,11)))
ck('Every QA row carries evidence for all 10 items',
   all(all(r[f'Q{i}_evidence'].strip() for i in range(1,11)) for r in qa))
selq=[r for r in qa if r['selected_for_final_50']=='YES']
ck('Exactly 50 studies flagged as selected', len(selq)==50, f'{len(selq)}')
ck('No selected study scores below 75', all(int(r['total_score_out_of_100'])>=75 for r in selq))
ck('Final-50 CSV has 50 rows', len(fin)==50, f'{len(fin)}')
ck('BibTeX CSV has 50 rows', len(bib)==50, f'{len(bib)}')
ck('Extraction table has 50 rows', len(ext)==50, f'{len(ext)}')
ck('Final-50 DOIs are unique', len({r['doi'] for r in fin})==50)
ck('BibTeX keys are unique', len({r['bibtex_key'] for r in bib})==50)
ck('Final-50 DOI set == BibTeX DOI set', {r['doi'] for r in fin}=={r['doi'] for r in bib})
ck('Final-50 DOI set == extraction DOI set', {r['doi'] for r in fin}=={r['doi'] for r in ext})
ck('Final-50 record_ids all appear in abstract screening as INCLUDE',
   {r['record_id'] for r in fin} <= {r['record_id'] for r in ai})
ck('All final-50 years are 2025 or 2026', all(r['year'] in ('2025','2026') for r in fin))
yrs=Counter(r['year'] for r in fin); ck('Year split 25/25', yrs['2025']==25 and yrs['2026']==25, str(dict(yrs)))
ck('All final-50 DOIs are well-formed', all(re.match(r'^10\.\d{4,9}/\S+$', r['doi']) for r in fin))
PRE={'10.48550','10.20944','10.21203','10.36227','10.2139','10.5281','10.33915','10.6028'}
ck('No preprint/self-archive DOI prefix in the final 50',
   not any(r['doi'].split('/')[0] in PRE for r in fin))
ck('No review/survey keyword in any final-50 title',
   not any(re.search(r'\b(survey|review|taxonomy|bibliometric)\b', r['title'], re.I) for r in fin))
reg=Counter(r['region'] for r in fin)
ck('EU/NA share >= 60%', reg['EU/NA']/50>=0.60, f"{reg['EU/NA']}/50 = {reg['EU/NA']*2}%")
th=Counter(r['theme'] for r in fin)
ck('Theme allocation 31/10/6/3', [th['T1_IDS_IOMT'],th['T2_FEDERATED_SECURITY'],th['T3_IMAGE_SECURITY'],th['T4_BLOCKCHAIN_HEALTHIOT']]==[31,10,6,3], str(dict(th)))
ck('Every extraction row names at least one dataset field value',
   all(r['dataset'].strip() for r in ext))
ck('Every extraction row declares its provenance', all(r['source'].strip() for r in ext))
ck('PRISMA counts file present', os.path.exists(B+'/04_PRISMA_Flow/01_prisma_flow_counts.csv'))
ck('PRISMA diagram present', os.path.exists(B+'/04_PRISMA_Flow/02_prisma_flow_diagram.png'))
ck('QA workbook present', os.path.exists(B+'/03_Screening/06_Quality_Assessment_Workbook.xlsx'))
ck('Extraction DOCX present', os.path.exists(B+'/05_Data_Extraction/02_metadata_extraction_all50.docx'))
ck('Paper tracker present', os.path.exists(B+'/Paper_Tracker.xlsx'))
_png=sorted(f for f in os.listdir(B+'/07_Figures') if f.endswith('.png'))
_pdf=sorted(f for f in os.listdir(B+'/07_Figures/vector_pdf') if f.endswith('.pdf'))
ck('Fourteen figures present as PNG', len(_png)==14, str(_png))
ck('Fourteen figures present as vector PDF', len(_pdf)==14, str(_pdf))
ck('Figure captions file present', os.path.exists(B+'/07_Figures/FIGURE_CAPTIONS.md'))
ck('Table captions file present', os.path.exists(B+'/06_Insight_Analysis/TABLE_CAPTIONS.md'))
ck('Thirteen analysis tables present',
   len([f for f in os.listdir(B+'/06_Insight_Analysis/Tables') if f.endswith('.csv')])==13)
import csv as _csv
_dsu={r['dataset']:int(r['n_studies_of_50']) for r in
      _csv.DictReader(io.open(B+'/06_Insight_Analysis/01_dataset_usage_frequency.csv',encoding='utf-8'))}
ck('Benchmark counts agree with the coded dataset', _dsu.get('CICIoMT2024')==11 and _dsu.get('WUSTL-EHMS-2020')==10,
   str(sorted(_dsu.items(),key=lambda x:-x[1])[:4]))
_t3=list(_csv.DictReader(io.open(B+'/06_Insight_Analysis/Tables/T03_benchmark_usage_and_verified_sizes.csv',encoding='utf-8')))
ck('Table 3 benchmark counts match the usage table',
   all(_dsu.get(r['Benchmark'])==int(r['n studies']) for r in _t3 if r['Benchmark'] in _dsu))

with open(B+'/04_PRISMA_Flow/03_verification_report.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['check','result','detail']); w.writerows(checks)
print(f'{sum(1 for c in checks if c[1]=="PASS")}/{len(checks)} checks passed')
for p in problems: print('  FAIL:',p)
