// Clear All Js Cache 

function clear_cache(){
    var rep = /.*\?.*/,
    scripts = document.getElementsByTagName('script'),

    process_scripts = true;

    if(process_scripts){
        
        for (var i=0;i<scripts.length;i++){

            var script = scripts[i],

            src = script.src;

            if(rep.test(src)){
                script.src = src+'&'+Date.now();

            }
            else{
                script.src = src+'?'+Date.now();

            }
        }
    }
}
setTimeout(clear_cache, 3000);