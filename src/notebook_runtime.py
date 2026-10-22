# Adaptação de infraestrutura para execução independente, sem clone obrigatório.
import functools, hashlib, importlib.metadata, inspect, json, marshal, types
from datetime import datetime, timezone
from pathlib import Path
MANIFEST = ROOT / 'outputs/logs/notebook_run_manifest.json'
_active = None
_written = set()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    temp.replace(path)

def verify_meridian_origin():
    origin = json.loads(importlib.metadata.distribution('google-meridian').read_text('direct_url.json') or '{}')
    if origin.get('vcs_info', {}).get('commit_id') != UPSTREAM_COMMIT or origin.get('url', '').rstrip('/') != 'https://github.com/google/meridian.git':
        raise RuntimeError('Origem/commit Meridian incompatível: instale a dependência fixada no início.')
    return origin

def fingerprint():
    versions = {p: importlib.metadata.version(p) for p in
                ['google-meridian', 'numpy', 'pandas', 'scipy', 'statsmodels', 'matplotlib', 'jax', 'tensorflow']}
    return {'raw_sha256': digest(RAW), 'versions': versions,
            'meridian_origin': verify_meridian_origin(),
            'configuration': [SEED, UPSTREAM_COMMIT, KPI, GEO, TIME, POP, CONTROLS, ORGANIC, NON_MEDIA]}

def code_state():
    # Cada etapa registra as funções já definidas. Redefini-las invalida a síntese.
    state = {}
    for name, value in list(globals().items()):
        if isinstance(value, types.FunctionType) and value.__module__ == __name__:
            function = inspect.unwrap(value)
            state[name] = hashlib.sha256(marshal.dumps(function.__code__)).hexdigest()
    return state

def record(path):
    if _active is not None:
        _written.add(str(Path(path).resolve().relative_to(ROOT)))

def require_stages(stages=range(7)):
    if not MANIFEST.exists():
        raise RuntimeError('Manifesto desta execução ausente. Execute o notebook de cima para baixo.')
    manifest = json.loads(MANIFEST.read_text())
    current, code = fingerprint(), code_state()
    for stage in stages:
        info = manifest.get('stages', {}).get(f'{stage:02}', {})
        if info.get('status') != 'complete' or info.get('fingerprint') != current:
            raise RuntimeError(f'Etapa {stage:02} ausente/desatualizada; reexecute.')
        if any(code.get(k) != v for k, v in info.get('code_hashes', {}).items()):
            raise RuntimeError(f'Código alterado após a etapa {stage:02}; reexecute desde o início.')
        for name, checksum in info['files'].items():
            if not (ROOT/name).exists() or digest(ROOT/name) != checksum:
                raise RuntimeError(f'Output alterado/ausente: {name}')
    return manifest

def tracked(stage):
    def decorate(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            global _active, _written
            if _active is not None:
                raise RuntimeError('Etapas aninhadas não suportadas')
            _active, _written = stage, set()
            manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'stages': {}}
            info = {'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
                    'original_source_commit': SOURCE_COMMIT, 'fingerprint': fingerprint(),
                    'code_hashes': code_state()}
            manifest['stages'][stage] = info
            write_json(MANIFEST, manifest)
            try:
                result = function(*args, **kwargs)
                if fingerprint() != info['fingerprint']:
                    raise RuntimeError('Dados/configuração/ambiente mudaram durante a etapa.')
                info.update(status='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                            files={p: digest(ROOT/p) for p in sorted(_written)})
                return result
            except Exception as exc:
                info.update(status='failed', error=str(exc))
                raise
            finally:
                manifest['stages'][stage] = info
                write_json(MANIFEST, manifest)
                _active, _written = None, set()
        return wrapped
    return decorate

def show(report, part='all'):
    from IPython.display import display, Markdown, Image
    if part in ['all', 'summary']:
        display(Markdown(report['narrative']))
    if part == 'summary':
        return
    for name, frame in report['tables'].items():
        display(Markdown(f'**{name}** — {len(frame)} linhas.'))
        with pd.option_context('display.max_rows', 60, 'display.max_columns', None):
            if len(frame) <= 50:
                display(frame)
            else:
                display(Markdown('Primeiras 12 linhas; a síntese interpreta a tabela completa. O CSV integral é exportado automaticamente.'))
                display(frame.head(12))
    for path in report['figures']:
        display(Markdown(figure_comment(path)))
        display(Image(filename=str(path), width=950))
