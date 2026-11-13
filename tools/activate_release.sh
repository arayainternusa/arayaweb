#!/usr/bin/env bash
# Activate only an already validated/uploaded package; roll back on failed live checks.
set -euo pipefail
[[ "$PRODUCTION_SSH_HOST" =~ ^[A-Za-z0-9][A-Za-z0-9.-]*$ ]]
[[ "$PRODUCTION_SSH_USER" =~ ^[a-z_][a-z0-9_-]{0,31}$ ]]
[[ "$PRODUCTION_SSH_PORT" =~ ^[0-9]{1,5}$ ]]
(( 10#$PRODUCTION_SSH_PORT > 0 && 10#$PRODUCTION_SSH_PORT <= 65535 ))
umask 077
ssh_dir=$(mktemp -d "$RUNNER_TEMP/araya-live-ssh.XXXXXX")
cleanup() { rm -f "$ssh_dir/key" "$ssh_dir/known_hosts"; rmdir "$ssh_dir"; }
trap cleanup EXIT
printf '%s\n' "$PRODUCTION_SSH_KEY" > "$ssh_dir/key"
printf '%s\n' "$PRODUCTION_KNOWN_HOSTS" > "$ssh_dir/known_hosts"
unset PRODUCTION_SSH_KEY PRODUCTION_KNOWN_HOSTS
options=(-i "$ssh_dir/key" -o "UserKnownHostsFile=$ssh_dir/known_hosts" -o StrictHostKeyChecking=yes
  -o BatchMode=yes -o IdentitiesOnly=yes -o IdentityAgent=none -o PasswordAuthentication=no
  -o ClearAllForwardings=yes -o ConnectTimeout=15 -o ServerAliveInterval=15 -o ServerAliveCountMax=2)
target="$PRODUCTION_SSH_USER@$PRODUCTION_SSH_HOST"

rollback() {
  ssh -p "$PRODUCTION_SSH_PORT" "${options[@]}" "$target" "bash -s -- '$release_id'" <<'REMOTE'
set -euo pipefail
id=$1
[[ "$id" =~ ^[a-f0-9]{40}-[1-9][0-9]*-[1-9][0-9]*$ ]]
root="$HOME/public_html"
public="$HOME/araya-static"
base="$HOME/araya-deploy"
test "$(cd "$root" && pwd -P)" = "$root"
test "$(cd "$base" && pwd -P)" = "$base"
if [[ ! -L "$public/.araya-current" || "$(readlink "$public/.araya-current")" != "releases/$id" ]]; then
  printf 'Expected release is not current; refusing rollback.\n' >&2; exit 1
fi
old=$(php -r '$r=json_decode(file_get_contents($argv[1]),true,512,JSON_THROW_ON_ERROR); echo $r["previous"]??"";' "$base/records/$id.json")
if [[ -n "$old" ]]; then
  [[ "$old" =~ ^releases/[a-f0-9]{40}-[1-9][0-9]*-[1-9][0-9]*$ ]]
  hash=$(printf '%s' "$old" | sha256sum); pointer="$public/.araya-next-${hash%% *}"
  if [[ -L "$pointer" ]]; then test "$(readlink "$pointer")" = "$old"; else test ! -e "$pointer"; ln -s "$old" "$pointer"; fi
fi
php "$base/incoming/$id/deploy_release.php" rollback "$id"
REMOTE
}

if [[ "${DEPLOY_MODE:-deploy}" = rollback ]]; then
  release_id="$ROLLBACK_RELEASE_ID"
  [[ "$release_id" =~ ^[a-f0-9]{40}-[1-9][0-9]{0,19}-[1-9][0-9]{0,9}$ ]]
  rollback
  printf '### Rolled back\n\nExpected release: `%s`\n\nPrevious pointer and routing restored. Verify the restored site.\n' "$release_id" >> "$GITHUB_STEP_SUMMARY"
  exit 0
fi

[[ "$BUILD_SHA" =~ ^[a-f0-9]{40}$ && "$ARCHIVE_SHA" =~ ^[a-f0-9]{64}$ && "$MANIFEST_SHA" =~ ^[a-f0-9]{64}$ ]]
remote_path=$(python tools/release_candidate.py destination "$PRODUCTION_SSH_USER" "$BUILD_SHA" "$GITHUB_RUN_ID" "$GITHUB_RUN_ATTEMPT")
release_id=${remote_path##*/}
# Recheck immediately before live activation; never allow a queued old build to replace main.
current_main=$(gh api "repos/$GITHUB_REPOSITORY/commits/main" --jq .sha)
if [[ "$current_main" != "$BUILD_SHA" ]]; then
  printf '::notice::Newer main commit exists; this candidate will not activate.\n'; exit 0
fi
scp -q -P "$PRODUCTION_SSH_PORT" "${options[@]}" tools/deploy_release.php tools/production.htaccess "$target:$remote_path/"
activated=true
recover() {
  status=$?
  (( status != 0 )) || status=130
  if [[ "${activated:-false}" = true ]]; then
    printf 'Activation/verification failed or interrupted; attempting guarded rollback.\n' >&2
    rollback || printf '::error::Rollback did not run; check the current release and hosting record immediately.\n' >&2
  fi
  exit "$status"
}
trap recover ERR INT TERM
ssh -p "$PRODUCTION_SSH_PORT" "${options[@]}" "$target" "bash -s -- '$release_id' '$ARCHIVE_SHA' '$MANIFEST_SHA'" <<'REMOTE'
set -euo pipefail
id=$1
root="$HOME/public_html"
public="$HOME/araya-static"
test "$(cd "$root" && pwd -P)" = "$root"
test ! -L "$public"
if [[ ! -d "$public" ]]; then mkdir -m 755 "$public"; fi
test "$(cd "$public" && pwd -P)" = "$public"
for name in index.html assets noris comap marine industrial automation privacy robots.txt sitemap.xml instalasi-fire-alarm \
  perbaikan-kapal perbaikan-kelistrikan-kapal perbaikan-mesin-kapal \
  retrofit-kontrol-monitoring-kapal perbaikan-kemudi-manuver-kapal perbaikan-crane-kapal-industri; do
  alias="$root/$name"; expected="../araya-static/.araya-current/$name"
  if [[ -L "$alias" ]]; then test "$(readlink "$alias")" = "$expected"; else test ! -e "$alias"; ln -s "$expected" "$alias"; fi
done
# Reserve the old pointer too: PHP cannot recreate it if routing installation fails.
if [[ -L "$public/.araya-current" ]]; then
  old=$(readlink "$public/.araya-current")
  [[ "$old" =~ ^releases/[a-f0-9]{40}-[1-9][0-9]*-[1-9][0-9]*$ ]]
  hash=$(printf '%s' "$old" | sha256sum); pointer="$public/.araya-next-${hash%% *}"
  if [[ -L "$pointer" ]]; then test "$(readlink "$pointer")" = "$old"; else test ! -e "$pointer"; ln -s "$old" "$pointer"; fi
fi
new="releases/$id"
hash=$(printf '%s' "$new" | sha256sum); pointer="$public/.araya-next-${hash%% *}"
if [[ -L "$pointer" ]]; then test "$(readlink "$pointer")" = "$new"; else test ! -e "$pointer"; ln -s "$new" "$pointer"; fi
php "$HOME/araya-deploy/incoming/$id/deploy_release.php" activate "$id" "$2" "$3"
REMOTE
python tools/check_live.py payload/release.json --attempts 5
activated=false
trap - ERR INT TERM
printf '### Production deployed and verified\n\nSource: `%s`\n\nRelease ID: `%s`\n\nBuild run: `%s`\n\nAll public file hashes, SEO/indexing, redirects and protected paths passed.\n' "$BUILD_SHA" "$release_id" "$BUILD_RUN_ID" >> "$GITHUB_STEP_SUMMARY"
