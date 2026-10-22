# Referência da verificação da consolidação. Executar na pasta pai que contenha
# original/ (snapshot do commit de origem) e MMM_Google_Meridian_Project2/.
# Requer pandas, numpy, scipy, matplotlib, statsmodels, tabulate e nbformat.
# Não é um ponto de entrada da análise; para estudar/recalcular, use o notebook.
from pathlib import Path
import ast, copy, hashlib, inspect, json, shutil, sys
import nbformat
import numpy as np
import pandas as pd
BASE=Path.cwd();NEW=BASE/'MMM_Google_Meridian_Project2';OLD=BASE/'original';RUN=BASE/'validation_run';RUN.mkdir(exist_ok=True)
shutil.copytree(OLD/'data',RUN/'data',dirs_exist_ok=True)
n=nbformat.read(NEW/'notebooks/01_EDA_COMPLETA.ipynb',as_version=4);nbformat.validate(n)
transfers=json.loads((NEW/'data/metadata/consolidation_source.json').read_text())['function_transfers']
class Normalize(ast.NodeTransformer):
 def visit_ImportFrom(self,node):return None if node.level else node
 def visit_Attribute(self,node):
  if isinstance(node.value,ast.Name) and node.value.id=='plots':return ast.Name(id=node.attr,ctx=node.ctx)
  return self.generic_visit(node)
found={}
for c in n.cells:
 if c.cell_type=='code':
  compile(c.source,'notebook','exec')
  for node in ast.parse(c.source).body:
   if isinstance(node,ast.FunctionDef):found[node.name]=node
checks=[]
for t in transfers:
 source=ast.parse((OLD/'src'/f"{t['module']}.py").read_text())
 f=next(x for x in source.body if isinstance(x,ast.FunctionDef) and x.name==t['function'])
 expected=Normalize().visit(copy.deepcopy(f));actual=found[t['function']]
 assert ast.dump(expected,include_attributes=False)==ast.dump(actual,include_attributes=False),t
 checks.append(t['function'])
assert (NEW/'docs/EDA_DIDACTIC_GUIDE.md').read_bytes()==(OLD/'docs/EDA_DIDACTIC_GUIDE.md').read_bytes()
print('PASS AST:',len(checks),'functions; notebook schema and all code cells compile; guide byte-identical.',flush=True)
namespace={'__name__':'__main__','PROJECT_ROOT':RUN,'SOURCE_COMMIT':'ef39d0a7629e849d31582cea6cefccb581f7a445'}
reports={}
for i,c in enumerate(n.cells):
 if c.cell_type!='code':continue
 tag=c.metadata.get('eda_role','')
 if tag in ['bootstrap','official_html','export'] or tag.startswith('evidence:'):continue
 if tag.startswith('run:'):
  stage=tag.split(':')[1]
  if int(stage)>=6:continue
  name=['data_audit','general','temporal','geo_analysis','media_geo','relationships'][int(stage)]
  print('RUN',stage,name,flush=True)
  reports[stage]=inspect.unwrap(namespace[name])(namespace['geo_time_panel'])
  print('PASS',stage,flush=True)
 else:exec(compile(c.source,f'notebook_cell_{i}','exec'),namespace)
# Compare every table produced by the six migrated stages against preserved originals.
comparisons=[]
for p in sorted((RUN/'outputs/tables').glob('*.csv')):
 ref=OLD/'outputs/tables'/p.name
 assert ref.exists(),p.name
 a,b=pd.read_csv(p),pd.read_csv(ref)
 pd.testing.assert_frame_equal(a,b,check_dtype=False,rtol=1e-10,atol=1e-9)
 comparisons.append(p.name)
print('PASS numeric comparison:',len(comparisons),'tables',flush=True)
# Test runtime stale-code and stale-artifact detection independently of Meridian installation.
namespace['fingerprint']=lambda:{'raw_sha256':namespace['digest'](namespace['RAW'])}
exec("@tracked('00')\ndef provenance_probe():\n    p=ROOT/'outputs/probe.txt'\n    p.write_text('ok')\n    record(p)\n",namespace)
namespace['provenance_probe']();namespace['require_stages']([0])
(RUN/'outputs/probe.txt').write_text('changed')
try:namespace['require_stages']([0]);raise AssertionError('altered artifact accepted')
except RuntimeError as e:assert 'Output alterado' in str(e)
namespace['provenance_probe']()
exec("def provenance_probe():\n    return 'changed'\n",namespace)
try:namespace['require_stages']([0]);raise AssertionError('altered function accepted')
except RuntimeError as e:assert 'Código alterado' in str(e)
# Ensure each source SVG is embedded once and the guide/source/outputs are identical.
embedded=[o.metadata['eda_source_path'] for c in n.cells for o in c.get('outputs',[]) if 'eda_source_path' in o.get('metadata',{})]
assert len(embedded)==len(set(embedded))==79
files=[]
for folder in ['data','outputs','docs','src']:
 for p in (OLD/folder).rglob('*'):
  if p.is_file():
   target=NEW/p.relative_to(OLD)
   assert target.read_bytes()==p.read_bytes(),str(p)
   files.append(str(p.relative_to(OLD)))
result={'source_commit':namespace['SOURCE_COMMIT'],'schema_valid':True,'all_code_cells_compile':True,'analytical_functions_AST_equivalent':len(checks),'functions':checks,'original_files_byte_identical':len(files),'figures_embedded':len(embedded),'six_custom_stages_executed':True,'tables_numerically_equal':len(comparisons),'comparison_tolerance':{'rtol':1e-10,'atol':1e-9},'compared_tables':comparisons,'provenance_modified_artifact_rejected':True,'provenance_modified_function_rejected':True,'official_meridian_reexecuted':False,'conclusions_execution_repeated':False,'colab_service_validated':False,'historical_outputs_retained':True}
(NEW/'data/metadata/consolidation_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['functions','compared_tables']},ensure_ascii=False),flush=True)
# Inspection image from the exact embedded data.
import base64
for c in n.cells:
 for o in c.get('outputs',[]):
  p=o.get('metadata',{}).get('eda_source_path','')
  if p.endswith(('geo_time_r2.svg','Channel2_impression_pc_geo_time.svg')):
   (BASE/'work'/Path(p).with_suffix('.png').name).write_bytes(base64.b64decode(o['data']['image/png']))
