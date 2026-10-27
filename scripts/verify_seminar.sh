#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD/seminario-featherweight-java"

echo "== Interpretador e type checker FJ"
python3 "$ROOT/exemplos/fj_trace.py"

echo "== Exemplos Java"
rm -rf /tmp/fj-example /tmp/fj-animals
mkdir -p /tmp/fj-example /tmp/fj-animals
if command -v javac >/dev/null && command -v java >/dev/null && javac -version >/dev/null 2>&1 && java -version >/dev/null 2>&1; then
  JAVAC=(javac); JAVA=(java)
elif command -v mise >/dev/null; then
  JAVAC=(mise x java@21 -- javac); JAVA=(mise x java@21 -- java)
else
  echo "JDK 17+ ou mise é necessário" >&2; exit 1
fi
"${JAVAC[@]}" -d /tmp/fj-example "$ROOT"/exemplos/src/*.java
"${JAVA[@]}" -cp /tmp/fj-example Main
"${JAVAC[@]}" -d /tmp/fj-animals "$ROOT"/exemplos/animais/*.java
"${JAVA[@]}" -cp /tmp/fj-animals MainAnimais

echo "== Links locais"
python3 - "$ROOT" <<'PY'
import pathlib,re,sys
root=pathlib.Path(sys.argv[1]); errors=[]
for p in root.rglob('*.md'):
 for t in re.findall(r'\[[^]]*\]\(([^)]+)\)',p.read_text()):
  if t.startswith(('http://','https://','#','mailto:')): continue
  if not (p.parent/t.split('#')[0]).exists(): errors.append(f'{p}: {t}')
h=root/'apresentacao/index.html'
for t in re.findall(r'(?:src|href)="([^"]+)"',h.read_text()):
 if t.startswith(('http://','https://','#')): continue
 if not (h.parent/t).exists(): errors.append(f'{h}: {t}')
if errors: print('\n'.join(errors)); raise SystemExit(1)
print('links/assets: ok')
PY

echo "== Deck"
node scripts/check_deck.mjs "$ROOT/apresentacao/index.html"
