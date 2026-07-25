async function analyze(){

    const url=document.getElementById("url").value;

    document.getElementById("loading").innerHTML="Analyzing...";

    const response = await fetch("/analyze", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            url:url
        })

    });

    const data=await response.json();

    document.getElementById("loading").innerHTML="";

    let html="";

    const icons = {

    "HTTP Status":"🌐",

    "Response Time (ms)":"⚡",

    "Title":"📰",

    "Meta Description":"📝",

    "H1 Count":"📌",

    "Approximate Word Count":"📖",

    "Images Missing Alt":"🖼️"

};

for(let key in data){

    html += `
    <div class="card">

        <b>${icons[key] || "📊"} ${key}</b>

        <span>${data[key]}</span>

    </div>
    `;

}

    document.getElementById("result").innerHTML=html;

}