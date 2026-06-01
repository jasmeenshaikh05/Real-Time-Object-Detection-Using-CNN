import React,{useRef,useEffect,useState} from "react";
import introVideo from "../assets/intro.mp4";
import logo from "../assets/panther_logo.png";

function LoadingScreen({onFinish}){

const videoRef=useRef(null);

const [showLogo,setShowLogo]=useState(false);
const [zoom,setZoom]=useState(false);
const [fade,setFade]=useState(false);

useEffect(()=>{

const video=videoRef.current;

if(!video) return;

video.play().catch(()=>{});

const handleTime=()=>{

const t=video.currentTime;

/* logo appears */

if(t>=3 && !showLogo){
setShowLogo(true);
}

/* zoom video + logo */

if(t>=6 && !zoom){
setZoom(true);
}

/* fade whole intro */

if(t>=8 && !fade){
setFade(true);
}

/* open dashboard */

if(t>=9.5){
onFinish();
}

};

video.addEventListener("timeupdate",handleTime);

return()=>{
video.removeEventListener("timeupdate",handleTime);
};

},[onFinish,showLogo,zoom,fade]);

return(

<div className={`intro-screen ${zoom?"zooming":""} ${fade?"fading":""}`}>

<video
ref={videoRef}
className="intro-video"
muted
autoPlay
playsInline
>
<source src={introVideo} type="video/mp4"/>
</video>

{showLogo && (

<div className="intro-overlay">

<img
src={logo}
className="intro-logo"
alt="PantherAI"
/>

<div className="intro-text">
Starting PantherAI...
</div>

</div>

)}

</div>

);

}

export default LoadingScreen;