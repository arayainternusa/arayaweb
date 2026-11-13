<?php
// Isolated filesystem fixtures: never use the real hosting document root.
require __DIR__ . '/deploy_release.php';
function check($ok, $message) { if (!$ok) throw new RuntimeException($message); }
function rejects($fn) { try { $fn(); } catch (Throwable $e) { return; } throw new RuntimeException('Expected refusal'); }
$folder = sys_get_temp_dir() . '/araya-test-' . bin2hex(random_bytes(6));
mkdir($folder, 0700);
try {
    check(safe_public_name('assets/site.css'), 'valid asset');
    foreach (['../index.html','assets/../secret.txt','assets/.env','wp-config.php','assets/x.php','/index.html','assets\\x.js'] as $bad) {
        check(!safe_public_name($bad), 'unsafe publication name accepted');
    }
    check(valid_release_id(str_repeat('a',40).'-123-1'), 'valid release');
    check(!valid_release_id('../bad') && !valid_release_id(str_repeat('a',40).'-0-1'), 'bad release accepted');
    $payload = $folder . '/payload'; mkdir($payload);
    $sha = str_repeat('a',40);
    $files = ['index.html'=>'home','noris/index.html'=>'noris','comap/index.html'=>'comap',
        'noris/id/index.html'=>'noris id','comap/id/index.html'=>'comap id','privacy/index.html'=>'privacy','instalasi-fire-alarm/index.html'=>'fire alarm',
        'perbaikan-kapal/index.html'=>'ship repair',
        'perbaikan-kelistrikan-kapal/index.html'=>'ship electrical',
        'perbaikan-mesin-kapal/index.html'=>'ship engine repair',
        'retrofit-kontrol-monitoring-kapal/index.html'=>'control retrofit',
        'perbaikan-kemudi-manuver-kapal/index.html'=>'steering and manoeuvring',
        'perbaikan-crane-kapal-industri/index.html'=>'marine and industrial cranes',
        'marine/index.html'=>'marine','industrial/index.html'=>'industrial','automation/index.html'=>'automation',
        'robots.txt'=>'robots','sitemap.xml'=>'sitemap','assets/site.css'=>'css','assets/site.js'=>'js',
        'assets/company-date.js'=>'date','assets/service-redirect.js'=>'redirect','assets/measurement.js'=>'measurement','assets/measurement.css'=>'consent styles',
        'assets/fonts/space-grotesk.woff2'=>'font','assets/fonts/OFL.txt'=>'licence'];
    function package_fixture($payload, $sha, $files) {
        $z=new ZipArchive(); $z->open($payload.'/araya-production.zip',ZipArchive::CREATE|ZipArchive::OVERWRITE);
        $hashes=[]; foreach ($files as $n=>$v) {$z->addFromString($n,$v); $hashes[$n]=hash('sha256',$v);} $z->close();
        $m=['source_commit'=>$sha,'source_tree_dirty'=>false,'target'=>'https://arayainternusa.co.id/',
            'archive'=>'araya-production.zip','archive_sha256'=>hash_file('sha256',$payload.'/araya-production.zip'),'files'=>$hashes];
        file_put_contents($payload.'/release.json',json_encode($m));
        return [$m['archive_sha256'],hash_file('sha256',$payload.'/release.json')];
    }
    [$a,$m]=package_fixture($payload,$sha,$files);
    check(count(verify_package($payload,$sha,$a,$m)['files'])===count($files),'valid package failed');
    rejects(function()use($payload,$sha,$m){verify_package($payload,$sha,str_repeat('0',64),$m);});
    $bad=$files; $bad['../escape.txt']='bad'; [$a,$m]=package_fixture($payload,$sha,$bad);
    rejects(function()use($payload,$sha,$a,$m){verify_package($payload,$sha,$a,$m);});
    [$a,$m]=package_fixture($payload,$sha,$files);
    $z=new ZipArchive(); $z->open($payload.'/araya-production.zip'); $z->setExternalAttributesName('assets/site.js',ZipArchive::OPSYS_UNIX,0120777<<16);$z->close();
    $data=json_decode(file_get_contents($payload.'/release.json'),true); $data['archive_sha256']=hash_file('sha256',$payload.'/araya-production.zip');file_put_contents($payload.'/release.json',json_encode($data));
    rejects(function()use($payload,$sha,$data){verify_package($payload,$sha,$data['archive_sha256'],hash_file('sha256',$payload.'/release.json'));});
    [$a,$m]=package_fixture($payload,$sha,$files);
    $data=json_decode(file_get_contents($payload.'/release.json'),true); $data['files']['index.html']=str_repeat('0',64);file_put_contents($payload.'/release.json',json_encode($data));
    rejects(function()use($payload,$sha,$a){verify_package($payload,$sha,$a,hash_file('sha256',$payload.'/release.json'));});
    echo "PASS package paths, provenance, hashes and symlink rejection\n";
    if (DIRECTORY_SEPARATOR === '/' && function_exists('symlink')) {
        $home=$folder.'/home'; mkdir($home);mkdir($home.'/public_html');mkdir($home.'/araya-deploy',0700);mkdir($home.'/araya-deploy/incoming',0700);
        file_put_contents($home.'/public_html/index.php',"<?php\n\nheader(\"Location: araya/\");\nexit;\n\n?>");
        mkdir($home.'/public_html/araya');file_put_contents($home.'/public_html/araya/wp-config.php','fixture, no credentials');
        $id=$sha.'-123-1'; $incoming=$home.'/araya-deploy/incoming/'.$id; mkdir($incoming,0700);
        [$a,$m]=package_fixture($incoming,$sha,$files);copy(__DIR__.'/production.htaccess',$incoming.'/production.htaccess');
        activate_release($home,$id,$a,$m);
        check(!file_exists($home.'/public_html/araya')&&is_file($home.'/araya-deploy/legacy/araya-'.$id.'/wp-config.php'),'legacy directory not privately retained');
        check(readlink($home.'/araya-static/.araya-current')==='releases/'.$id,'first pointer');
        // Force routing write failure after switching to another immutable release.
        $shaFail=str_repeat('c',40);$idFail=$shaFail.'-125-1';$failed=$home.'/araya-deploy/incoming/'.$idFail;mkdir($failed,0700);
        [$af,$mf]=package_fixture($failed,$shaFail,$files);copy(__DIR__.'/production.htaccess',$failed.'/production.htaccess');
        $reserved=$home.'/araya-static/.araya-next-'.hash('sha256','releases/'.$id);symlink('releases/'.$id,$reserved);
        chmod($home.'/public_html',0555);clearstatcache();
        try {if(!is_writable($home.'/public_html')){
            rejects(function()use($home,$idFail,$af,$mf){activate_release($home,$idFail,$af,$mf);});
            check(readlink($home.'/araya-static/.araya-current')==='releases/'.$id,'failed activation did not restore old pointer');
        }} finally {chmod($home.'/public_html',0755);}
        $sha2=str_repeat('b',40);$id2=$sha2.'-124-1';$incoming2=$home.'/araya-deploy/incoming/'.$id2;mkdir($incoming2,0700);
        [$a2,$m2]=package_fixture($incoming2,$sha2,$files);copy(__DIR__.'/production.htaccess',$incoming2.'/production.htaccess');
        file_put_contents($incoming2.'/production.htaccess',"\n# Fixture routing revision\n",FILE_APPEND);
        activate_release($home,$id2,$a2,$m2);
        rejects(function()use($home,$id){rollback_release($home,$id);});
        chmod($home.'/public_html',0555);clearstatcache();
        try {if(!is_writable($home.'/public_html')){
            rejects(function()use($home,$id2){rollback_release($home,$id2);});
            check(readlink($home.'/araya-static/.araya-current')==='releases/'.$id2,'failed rollback changed pointer');
            check(hash_file('sha256',$home.'/public_html/.htaccess')===hash_file('sha256',$incoming2.'/production.htaccess'),'failed rollback changed routing');
        }} finally {chmod($home.'/public_html',0755);}
        rollback_release($home,$id2);check(readlink($home.'/araya-static/.araya-current')==='releases/'.$id,'restore prior static release');
        rollback_release($home,$id);check(!is_link($home.'/araya-static/.araya-current')&&!file_exists($home.'/public_html/.htaccess'),'restore original root');
        check(is_file($home.'/public_html/araya/wp-config.php'),'legacy application was not restored');
        file_put_contents($home.'/public_html/.htaccess','unmanaged configuration');
        rejects(function()use($home,$id2,$a2,$m2){activate_release($home,$id2,$a2,$m2);});
        unlink($home.'/public_html/.htaccess');symlink('/tmp',$home.'/araya-static/.araya-current');
        rejects(function()use($home,$id2,$a2,$m2){activate_release($home,$id2,$a2,$m2);});
        echo "PASS atomic activation, stale rollback refusal, static/legacy rollback and filesystem guards\n";
    } else { echo "Activation fixtures require Linux symlink support; run in CI. Hosting uses SSH-prepared pointers.\n"; }
} finally {
    // Delete only the random isolated fixture tree created above, without following links.
    $it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($folder,FilesystemIterator::SKIP_DOTS),RecursiveIteratorIterator::CHILD_FIRST);
    foreach($it as $p){if($p->isLink()||$p->isFile())unlink($p->getPathname());else rmdir($p->getPathname());} rmdir($folder);
}
