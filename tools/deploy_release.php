<?php
// CLI deployment only. This file is never installed in the public document root.
function demand($ok, $why) { if (!$ok) throw new RuntimeException($why); }
function valid_release_id($id) {return preg_match('/\A[a-f0-9]{40}-[1-9][0-9]{0,19}-[1-9][0-9]{0,9}\z/',$id)===1;}
function safe_public_name($name) {
    if(!is_string($name)||preg_match('~(?:\A/|\\\\|(?:\A|/)\.|//)~',$name))return false;
    return in_array($name,['index.html','noris/index.html','comap/index.html','noris/id/index.html','comap/id/index.html','privacy/index.html','marine/index.html','industrial/index.html','automation/index.html','robots.txt','sitemap.xml','assets/fonts/OFL.txt'],true)
        ||preg_match('~\Aassets/[A-Za-z0-9_./-]+\.(?:css|js|svg|webp|png|jpg|jpeg|woff2|pdf)\z~',$name)===1;
}
function verify_package($dir,$sha,$archiveHash,$manifestHash) {
    demand(preg_match('/\A[a-f0-9]{40}\z/',$sha)&&preg_match('/\A[a-f0-9]{64}\z/',$archiveHash)&&preg_match('/\A[a-f0-9]{64}\z/',$manifestHash),'Invalid hashes');
    foreach(['release.json'=>2000000,'araya-production.zip'=>50000000] as $n=>$max){demand(!is_link($dir.'/'.$n)&&is_file($dir.'/'.$n)&&filesize($dir.'/'.$n)<=$max,'Invalid package file');}
    demand(hash_file('sha256',$dir.'/araya-production.zip')===$archiveHash&&hash_file('sha256',$dir.'/release.json')===$manifestHash,'Transport hash mismatch');
    $m=json_decode(file_get_contents($dir.'/release.json'),true,512,JSON_THROW_ON_ERROR);
    demand(($m['source_commit']??'')===$sha&&($m['source_tree_dirty']??null)===false&&($m['target']??'')==='https://arayainternusa.co.id/'&&($m['archive']??'')==='araya-production.zip'&&($m['archive_sha256']??'')===$archiveHash&&is_array($m['files']??null),'Invalid provenance');
    $required=['index.html','noris/index.html','comap/index.html','noris/id/index.html','comap/id/index.html','privacy/index.html','marine/index.html','industrial/index.html','automation/index.html','robots.txt','sitemap.xml','assets/site.css','assets/site.js','assets/measurement.js','assets/measurement.css','assets/company-date.js','assets/service-redirect.js','assets/fonts/space-grotesk.woff2','assets/fonts/OFL.txt'];
    demand(!array_diff($required,array_keys($m['files'])),'Incomplete release');
    foreach($m['files'] as $n=>$hash){demand(safe_public_name($n)&&preg_match('/\A[a-f0-9]{64}\z/',$hash),'Unsafe publication entry');}
    $z=new ZipArchive();demand($z->open($dir.'/araya-production.zip')===true,'Unreadable ZIP');
    try {
        demand($z->numFiles===count($m['files'])&&$z->numFiles<=5000,'Wrong ZIP entries');$seen=[];$size=0;
        for($i=0;$i<$z->numFiles;$i++){
            $s=$z->statIndex($i);$n=$s['name'];$size+=$s['size'];
            demand(isset($m['files'][$n])&&!isset($seen[$n])&&$size<=100000000,'Unexpected/duplicate ZIP entry');$seen[$n]=true;
            $ops=0;$attr=0;$z->getExternalAttributesIndex($i,$ops,$attr);
            demand((($attr>>16)&0170000)!==0120000,'ZIP symlink refused');
            $bytes=$z->getFromIndex($i);demand($bytes!==false&&hash('sha256',$bytes)===$m['files'][$n],'Inner file hash mismatch');
        }
    } finally {$z->close();}
    return $m;
}
function checked_layout($home) {
    demand(realpath($home)===$home&&!is_link($home),'Unsafe home');
    foreach(['public_html','araya-deploy','araya-deploy/incoming'] as $n){demand(realpath($home.'/'.$n)===$home.'/'.$n&&!is_link($home.'/'.$n),'Unsafe deployment layout');}
    return [$home.'/public_html',$home.'/araya-deploy'];
}
function mkdir_checked($path,$mode) {if(!file_exists($path)){demand(mkdir($path,$mode),'Cannot create directory');chmod($path,$mode);}demand(is_dir($path)&&!is_link($path)&&realpath($path)===$path,'Unsafe directory');}
function public_links() {return ['index.html','assets','noris','comap','marine','industrial','automation','privacy','robots.txt','sitemap.xml'];}
function public_layout($home,$root,$create=false) {
    $public=$home.'/araya-static';mkdir_checked($public,0755);mkdir_checked($public.'/releases',0755);
    foreach(public_links() as $name){
        $path=$root.'/'.$name;$target='../araya-static/.araya-current/'.$name;
        if(!is_link($path)){demand(!file_exists($path),'Unmanaged public path');if(!$create)continue;demand(function_exists('symlink'),'Static link must be prepared through SSH');demand(symlink($target,$path),'Cannot create static link');}
        demand(readlink($path)===$target,'Unmanaged public path');
    }
    return $public;
}
function pointer_target($root) {
    $p=$root.'/.araya-current';
    if(!is_link($p)){demand(!file_exists($p),'Unmanaged current path');return null;}
    $t=readlink($p);demand(preg_match('~\Areleases/([a-f0-9]{40}-[1-9][0-9]{0,19}-[1-9][0-9]{0,9})\z~',$t,$match)&&valid_release_id($match[1]),'Unsafe current pointer');
    demand(!is_link($root.'/'.$t)&&realpath($root.'/'.$t)===$root.'/'.$t,'Current release escapes root');return $t;
}
function atomic_bytes($path,$bytes,$mode) {
    $tmp=$path.'.tmp-'.bin2hex(random_bytes(6));
    try {demand(@file_put_contents($tmp,$bytes)!==false,'Cannot write temporary file');chmod($tmp,$mode);demand(rename($tmp,$path),'Cannot replace file');}
    finally {if(is_file($tmp))unlink($tmp);}
}
function switch_pointer($root,$target) {
    // Rumahweb disables PHP symlink(); the SSH wrapper prepares these links with ln.
    $temp=$root.'/.araya-next-'.hash('sha256',$target);
    if(!is_link($temp)){demand(!file_exists($temp)&&function_exists('symlink'),'Release pointer must be prepared through SSH');demand(symlink($target,$temp),'Cannot create release pointer');}
    demand(readlink($temp)===$target,'Prepared pointer has wrong target');demand(rename($temp,$root.'/.araya-current'),'Cannot switch release');clearstatcache();
}
function with_deploy_lock($home,$fn) {
    [$root,$base]=checked_layout($home);$lock=fopen($base.'/deploy.lock','c');demand($lock!==false&&flock($lock,LOCK_EX),'Cannot lock deployment');
    try {return $fn($root,$base);} finally {flock($lock,LOCK_UN);fclose($lock);}
}
function activate_release($home,$id,$archiveHash,$manifestHash) {
    demand(valid_release_id($id),'Invalid release ID');
    return with_deploy_lock($home,function($root,$base)use($home,$id,$archiveHash,$manifestHash){
        $homePublic=public_layout($home,$root);
        $incoming=$base.'/incoming/'.$id;demand(realpath($incoming)===$incoming&&!is_link($incoming),'Unsafe incoming directory');
        $sha=substr($id,0,40);$m=verify_package($incoming,$sha,$archiveHash,$manifestHash);
        $router=file_get_contents($incoming.'/production.htaccess');demand(strpos($router,'# Araya managed static routing v1')===0,'Unrecognised routing file');
        $previous=pointer_target($homePublic);$routerPath=$root.'/.htaccess';demand(!is_link($routerPath),'Router symlink refused');
        $oldRouter=is_file($routerPath)?file_get_contents($routerPath):null;
        mkdir_checked($base.'/records',0700);
        $legacyRelative=null;
        if($previous!==null){
            $prevId=basename($previous);$prevRecord=json_decode(file_get_contents($base.'/records/'.$prevId.'.json'),true,512,JSON_THROW_ON_ERROR);
            demand($oldRouter!==null&&hash('sha256',$oldRouter)===($prevRecord['router_sha256']??''),'Existing router was changed outside deployment');
        } else {
            demand($oldRouter===null,'Unmanaged root configuration; refusing overwrite');
            demand(is_file($root.'/index.php')&&!is_link($root.'/index.php')&&hash_file('sha256',$root.'/index.php')==='8305556db7c82cd97c81cb0dcae96d85b4334a039e25d14c2bb5da91f9c8e7ab','Original entry point changed');
            demand(realpath($root.'/araya')===$root.'/araya'&&!is_link($root.'/araya')&&is_file($root.'/araya/wp-config.php'),'Expected legacy WordPress directory missing');
            mkdir_checked($base.'/legacy',0700);$legacyRelative='legacy/araya-'.$id;
            demand(!file_exists($base.'/'.$legacyRelative)&&!is_link($base.'/'.$legacyRelative),'Legacy destination already exists');
        }
        public_layout($home,$root,true);
        mkdir_checked($homePublic.'/releases',0755);$release=$homePublic.'/releases/'.$id;
        demand(!file_exists($release)&&!is_link($release)&&!file_exists($base.'/records/'.$id.'.json'),'Release ID already used');
        $site=$incoming.'/site';demand(!file_exists($site)&&!is_link($site),'Extraction path already exists');demand(mkdir($site,0700),'Cannot create site');
        $z=new ZipArchive();demand($z->open($incoming.'/araya-production.zip')===true,'Cannot reopen ZIP');
        try {foreach($m['files'] as $n=>$hash){$dest=$site.'/'.$n;$parent=$site;foreach(explode('/',dirname($n)) as $part){if($part!=='.'){$parent.='/'.$part;mkdir_checked($parent,0755);}}demand(file_put_contents($dest,$z->getFromName($n))!==false,'Cannot write release');chmod($dest,0644);demand(hash_file('sha256',$dest)===$hash,'Extracted hash mismatch');}} finally {$z->close();}
        demand(rename($site,$release),'Cannot install release');chmod($release,0755);
        $record=['id'=>$id,'source_commit'=>$sha,'previous'=>$previous,'legacy_relative'=>$legacyRelative,'previous_router_base64'=>$oldRouter===null?null:base64_encode($oldRouter),'router_sha256'=>hash('sha256',$router),'manifest_sha256'=>$manifestHash,'activated_utc'=>gmdate('c')];
        atomic_bytes($base.'/records/'.$id.'.json',json_encode($record,JSON_PRETTY_PRINT)."\n",0600);
        // Initial cutover config points at the new static site, then the pointer is replaced atomically.
        try {switch_pointer($homePublic,'releases/'.$id);atomic_bytes($routerPath,$router,0644);if($legacyRelative!==null)demand(rename($root.'/araya',$base.'/'.$legacyRelative),'Cannot move legacy application to private storage');}
        catch(Throwable $e){if($legacyRelative!==null&&is_dir($base.'/'.$legacyRelative)&&!file_exists($root.'/araya'))demand(rename($base.'/'.$legacyRelative,$root.'/araya'),'Cannot restore legacy application');if($previous===null){if(is_link($homePublic.'/.araya-current'))unlink($homePublic.'/.araya-current');}else {switch_pointer($homePublic,$previous);}if($oldRouter===null){if(is_file($routerPath))unlink($routerPath);}elseif(!is_file($routerPath)||file_get_contents($routerPath)!==$oldRouter){atomic_bytes($routerPath,$oldRouter,0644);}throw $e;}
        return $record;
    });
}
function rollback_release($home,$expected) {
    demand(valid_release_id($expected),'Invalid rollback release');
    return with_deploy_lock($home,function($root,$base)use($home,$expected){
        $homePublic=public_layout($home,$root);
        demand(pointer_target($homePublic)==='releases/'.$expected,'Current release changed; refusing stale rollback');
        $record=json_decode(file_get_contents($base.'/records/'.$expected.'.json'),true,512,JSON_THROW_ON_ERROR);
        demand(($record['id']??'')===$expected&&!is_link($root.'/.htaccess')&&hash_file('sha256',$root.'/.htaccess')===$record['router_sha256'],'Routing changed; refusing rollback');
        $old=$record['previous'];$oldRouter=$record['previous_router_base64']===null?null:base64_decode($record['previous_router_base64'],true);
        if($old!==null){
            demand(preg_match('~\Areleases/([a-f0-9]{40}-[1-9][0-9]{0,19}-[1-9][0-9]{0,9})\z~',$old)&&realpath($homePublic.'/'.$old)===$homePublic.'/'.$old&&!is_link($homePublic.'/'.$old),'Unsafe rollback target');
            $oldId=basename($old);$oldRecord=json_decode(file_get_contents($base.'/records/'.$oldId.'.json'),true,512,JSON_THROW_ON_ERROR);
            $oldManifestPath=$base.'/incoming/'.$oldId.'/release.json';
            demand(!is_link($oldManifestPath)&&hash_file('sha256',$oldManifestPath)===$oldRecord['manifest_sha256'],'Previous manifest changed');
            $oldManifest=json_decode(file_get_contents($oldManifestPath),true,512,JSON_THROW_ON_ERROR);
            foreach($oldManifest['files'] as $n=>$hash){$p=$homePublic.'/'.$old.'/'.$n;demand(safe_public_name($n)&&realpath($p)===$p&&!is_link($p)&&hash_file('sha256',$p)===$hash,'Previous release file changed');}
            demand($oldRouter!==null&&$oldRouter!==false,'Missing previous routing');
            $currentRouter=file_get_contents($root.'/.htaccess');
            try {if($currentRouter!==$oldRouter)atomic_bytes($root.'/.htaccess',$oldRouter,0644);switch_pointer($homePublic,$old);}
            catch(Throwable $e){if(file_get_contents($root.'/.htaccess')!==$currentRouter)atomic_bytes($root.'/.htaccess',$currentRouter,0644);throw $e;}
        } else {
            demand($oldRouter===null,'Unexpected original router');
            demand(hash_file('sha256',$root.'/index.php')==='8305556db7c82cd97c81cb0dcae96d85b4334a039e25d14c2bb5da91f9c8e7ab','Original PHP changed');
            $legacyRelative=$record['legacy_relative']??null;
            if($legacyRelative!==null){
                demand($legacyRelative==='legacy/araya-'.$expected&&realpath($base.'/'.$legacyRelative)===$base.'/'.$legacyRelative&&!is_link($base.'/'.$legacyRelative),'Unsafe legacy restore path');
                demand(!file_exists($root.'/araya')&&!is_link($root.'/araya'),'Legacy root path is occupied');
                demand(is_writable($root)&&is_writable($base.'/legacy'),'Cannot restore legacy routing safely');
                demand(rename($base.'/'.$legacyRelative,$root.'/araya'),'Cannot restore legacy application');
            }
            demand(unlink($root.'/.htaccess'),'Cannot restore original routing');demand(unlink($homePublic.'/.araya-current'),'Cannot remove initial pointer');
            foreach(public_links() as $name){demand(readlink($root.'/'.$name)==='../araya-static/.araya-current/'.$name,'Public link changed');demand(unlink($root.'/'.$name),'Cannot remove managed link');}
        }
        return ['rolled_back'=>$expected,'restored'=>$old];
    });
}
if(realpath($_SERVER['SCRIPT_FILENAME']??'')===__FILE__){
    try {
        demand(PHP_SAPI==='cli','CLI only');$home=getenv('HOME');demand(preg_match('~\A/home/[a-z_][a-z0-9_-]{0,31}\z~',$home),'Invalid account home');umask(0077);
        $action=$argv[1]??'';
        if($action==='activate'&&count($argv)===5)$result=activate_release($home,$argv[2],$argv[3],$argv[4]);
        elseif($action==='rollback'&&count($argv)===3)$result=rollback_release($home,$argv[2]);
        else throw new RuntimeException('Invalid command');
        echo json_encode($result,JSON_UNESCAPED_SLASHES)."\n";
    }catch(Throwable $e){fwrite(STDERR,'Deployment refused: '.$e->getMessage()."\n");exit(1);}
}
