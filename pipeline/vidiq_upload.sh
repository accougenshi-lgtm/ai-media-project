#!/bin/sh
# Resumable upload to vidIQ storage (same logic as the command vidIQ's vidiq_video_upload returns).
# Usage: sh pipeline/vidiq_upload.sh <file> <size_bytes> <signed_upload_url> <content_type> <upload_id>
set -u; umask 077
F="$1"; N="$2"; U="$3"; T="$4"; ID="$5"; S="${TMPDIR:-/tmp}/vidiq-upload-$ID"
fail() { printf "vidIQ upload stopped: %s\n" "$*" >&2; exit 1; }
c() { curl -q -sS -g --connect-timeout 30 "$@"; }
code() { tr -d "\r" | sed -n "s/^HTTP\/[0-9.]* \([0-9][0-9][0-9]\).*/\1/p" | tail -n 1; }
hdr() { tr -d "\r" | grep -i "^$1:" | tail -n 1 | sed "s/^[^:]*: *//"; }
status() { c -m 60 -o /dev/null -D - -X PUT -H "Content-Length: 0" -H "Content-Range: bytes */$N" "$X" || fail "lost connection; run again to resume."; }
[ -f "$F" ] && [ -r "$F" ] || fail "cannot read $F"
A=$(wc -c < "$F" | tr -d " "); [ "$A" = "$N" ] || fail "$F has $A bytes, not $N"
X=$(cat "$S" 2>/dev/null); Q=""
[ -n "$X" ] && { Q=$(status) || exit 1; }
case "$(printf "%s\n" "$Q" | code)" in 200|201|308|408|429|5??) ;; *) X="" ;; esac
if [ -z "$X" ]; then
  R=$(c -m 60 -o /dev/null -D - -X POST -H "x-goog-resumable: start" -H "x-upload-content-type: $T" -H "x-upload-content-length: $N" -H "Content-Length: 0" "$U") || fail "cannot reach storage.googleapis.com"
  X=$(printf "%s\n" "$R" | hdr location); [ -n "$X" ] || fail "upload link refused/expired; request a new one"
  printf "%s\n" "$X" > "$S" 2>/dev/null; Q=$(status) || exit 1
fi
case "$(printf "%s\n" "$Q" | code)" in
  200|201) ;;
  308) R=$(printf "%s\n" "$Q" | hdr range | sed "s/.*-//"); O=$(( ${R:--1} + 1 ))
       W=$(c -Y 1 -y 120 -o /dev/null -w "%{http_code}" -X PUT -C "$O" -T "$F" "$X")
       case "$W" in 200|201) ;; *) fail "interrupted; run again to resume." ;; esac ;;
  *) fail "unexpected storage answer; run again." ;;
esac
echo "vidIQ upload complete: $ID"
