import React,{useState,useRef,useEffect} from "react";

function Dashboard(){

const mainModules=[
"Object Detection",
"Hazard Detection"
];

const hazardModules=[
"Fire Detection",
"Weapon Detection",
"Crowd Density"
];

const [mode,setMode]=useState("main");
const [index,setIndex]=useState(0);
const [module,setModule]=useState("");
const [theme,setTheme]=useState("dark");
const [videoURL,setVideoURL]=useState("");

const [streamURL,setStreamURL]=useState("");
const [showStream,setShowStream]=useState(false);

const [alerts,setAlerts]=useState([]);

const startX=useRef(0);

const modules=mode==="main"?mainModules:hazardModules;


/* ✅ FIXED: use YOUR IP */
useEffect(()=>{

const interval=setInterval(()=>{

fetch("http://127.0.0.1:5000/alerts")
.then(res=>res.json())
.then(data=>setAlerts(data))
.catch(()=>{});

},2000);

return ()=>clearInterval(interval);

},[]);


/* rotation */

const rotateLeft=()=>{
setIndex((index-1+modules.length)%modules.length);
};

const rotateRight=()=>{
setIndex((index+1)%modules.length);
};


/* drag */

const handleDragStart=(e)=>{
startX.current=e.touches?e.touches[0].clientX:e.clientX;
};

const handleDragMove=(e)=>{

const currentX=e.touches?e.touches[0].clientX:e.clientX;
const diff=currentX-startX.current;

if(Math.abs(diff)>40){

if(diff>0) rotateLeft();
else rotateRight();

startX.current=currentX;

}

};

const active=modules[index];


/* MODULE SELECT */

const selectModule=()=>{

if(mode==="main" && active==="Hazard Detection"){
setMode("hazard");
setIndex(0);
setModule("");
setShowStream(false);
setStreamURL("");
return;
}

setModule(active);

setShowStream(false);
setStreamURL("");

setTimeout(()=>{

let url="";

/* ✅ FIXED: use YOUR IP everywhere */

if(active==="Weapon Detection"){
url="http://127.0.0.1:5000/detect/weapon";
}

if(active==="Fire Detection"){
url="http://127.0.0.1:5000/detect/fire";
}

if(active==="Crowd Density"){
url="http://127.0.0.1:5000/detect/crowd";
}

if(active==="Object Detection"){
url="http://127.0.0.1:5000/detect/object";
}

setStreamURL(url);

setTimeout(()=>{
setShowStream(true);
},500);

},300);

};


const goBack=()=>{
setMode("main");
setIndex(0);
setModule("");
setShowStream(false);
setStreamURL("");
};


return(

<div className={`dashboard ${theme}`}>

<header className="header">

<div>PantherAI Security Dashboard</div>

<button
className="theme-toggle"
onClick={()=>setTheme(theme==="dark"?"light":"dark")}
>
{theme==="dark"?"Light Mode":"Dark Mode"}
</button>

</header>


<div className="layout">


{/* SEMICIRCLE */}

<div
className="semicircle-wrapper"
onMouseDown={handleDragStart}
onMouseMove={(e)=>e.buttons===1 && handleDragMove(e)}
onTouchStart={handleDragStart}
onTouchMove={handleDragMove}
>

<button className="arrow arrow-left" onClick={rotateLeft}>
◀
</button>

<div className="semicircle">

{modules.map((m,i)=>{

const angle=(i-index)*50;

return(

<div
key={i}
className={`arc-item ${i===index?"active":""}`}
style={{
transform:`rotate(${angle}deg) translate(260px) rotate(${-angle}deg)`
}}
onClick={selectModule}
>

{m}

</div>

);

})}

</div>

<button className="arrow arrow-right" onClick={rotateRight}>
▶
</button>

</div>


{/* CENTER */}

<div className="center-view">

<h2>{module || active}</h2>

{mode==="hazard" && (

<button className="back-btn" onClick={goBack}>
← Back
</button>

)}

{module && (

<div className="video-controls">

<input
type="text"
placeholder="Paste YouTube video URL..."
value={videoURL}
onChange={(e)=>setVideoURL(e.target.value)}
/>

<button
className="detect-btn"
onClick={()=>{

if(!videoURL) return;

setShowStream(false);
setStreamURL("");

setTimeout(()=>{

setStreamURL(`http://10.195.254.161:5000/detect/youtube?url=${videoURL}`);

setTimeout(()=>{
setShowStream(true);
},500);

},300);

}}
>
Detect From YouTube
</button>

<button className="detect-btn">
Live Webcam
</button>

</div>

)}

<div className="camera-box">

{showStream && streamURL && (
<img
key={streamURL}
src={streamURL}
alt="Detection Stream"
style={{
width:"100%",
height:"100%",
objectFit:"cover",
borderRadius:"14px"
}}
/>
)}

</div>

</div>


{/* ALERT PANEL */}

<div className="alerts">

<h3>Security Alerts</h3>

{alerts.length===0 && (
<div className="alert">
Waiting for detections...
</div>
)}

{alerts.map((a,i)=>(
<div key={i} className="alert">
{a}
</div>
))}

<h3>Telegram Status</h3>

<div className="telegram">
{alerts.length>0 ? "Alert sent" : "No alerts yet"}
</div>

</div>

</div>

</div>

)

}

export default Dashboard;