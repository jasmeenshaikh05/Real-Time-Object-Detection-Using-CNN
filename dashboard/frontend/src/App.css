/* ================= GLOBAL ================= */

*{
box-sizing:border-box;
}

body{
margin:0;
font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
overflow-x:hidden;
background:black;
}

/* ================= INTRO ================= */

.intro-screen{

position:fixed;
top:0;
left:0;

width:100vw;
height:100vh;

background:black;

display:flex;
align-items:center;
justify-content:center;

overflow:hidden;

z-index:9999;

opacity:1;
transition:opacity 1.5s ease;
}

.fading{
opacity:0;
}

/* video */

.intro-video{

position:absolute;

width:100%;
height:100%;

object-fit:cover;

transition:transform 3s ease;
}

/* overlay */

.intro-overlay{

display:flex;
flex-direction:column;

align-items:center;
justify-content:center;

gap:22px;

z-index:2;
}

/* logo */

.intro-logo{

width:680px;

max-width:85%;

filter:drop-shadow(0 0 35px rgba(0,255,255,0.9));

transition:transform 3s ease;
}

/* intro text */

.intro-text{

font-size:18px;

letter-spacing:2px;

color:white;

animation:bootPulse 2s infinite;
}

@keyframes bootPulse{

0%{opacity:0.3}
50%{opacity:1}
100%{opacity:0.3}

}

/* zoom effect */

.zooming .intro-video{
transform:scale(1.3);
}

.zooming .intro-logo{
transform:scale(5);
}

/* ================= DASHBOARD ================= */

.dashboard{

height:100vh;

display:flex;
flex-direction:column;

position:relative;

color:white;
}

/* ================= BACKGROUND ================= */

.dashboard::before{

content:"";

position:absolute;

top:0;
left:0;

width:100%;
height:100%;

background-size:cover;
background-position:center;

filter:blur(22px) brightness(0.65);

transform:scale(1.1);

z-index:-1;
}

.dashboard.dark::before{
background-image:url("/panther_dark.jpg");
}

.dashboard.light::before{
background-image:url("/panther_light.jpg");
filter:blur(22px) brightness(0.9);
}

/* ================= HEADER ================= */

.header{

display:flex;
justify-content:space-between;
align-items:center;

padding:20px 30px;

font-size:22px;

border-bottom:1px solid rgba(255,255,255,0.1);

backdrop-filter:blur(10px);
}

/* ================= THEME BUTTON ================= */

.theme-toggle{

padding:8px 14px;

border:none;

border-radius:8px;

cursor:pointer;

font-weight:500;

background:#0ff;

transition:0.3s;
}

.theme-toggle:hover{

box-shadow:0 0 10px #0ff;
}

/* ================= MAIN LAYOUT ================= */

.layout{

flex:1;

display:flex;

align-items:center;

justify-content:space-between;

padding:20px;

gap:120px;
}

/* ================= SEMICIRCLE ================= */

.semicircle-wrapper{

width:500px;

height:100%;

display:flex;

align-items:center;

justify-content:center;

position:relative;

cursor:grab;
}

.semicircle{

width:560px;
height:560px;

border-radius:50%;

border:2px solid rgba(0,255,255,0.25);

position:absolute;

left:-280px;

box-shadow:

0 0 60px rgba(0,255,255,0.25),
inset 0 0 40px rgba(0,255,255,0.1);
}

/* arc buttons */

.arc-item{

position:absolute;

top:50%;
left:50%;

width:190px;

padding:14px;

text-align:center;

border-radius:12px;

cursor:pointer;

background:rgba(15,20,30,0.75);

border:1px solid rgba(0,255,255,0.2);

color:#ccc;

font-size:15px;

transition:all 0.35s ease;
}

.arc-item.active{

background:#0ff;

color:black;

box-shadow:

0 0 20px #0ff,
0 0 40px rgba(0,255,255,0.7);
}

.arc-item:hover{

transform:scale(1.05);

box-shadow:0 0 14px rgba(0,255,255,0.5);
}

/* ================= ARROWS ================= */

.arrow{

position:absolute;

top:50%;

transform:translateY(-50%);

font-size:22px;

border:none;

border-radius:6px;

padding:8px 12px;

cursor:pointer;

background:#0ff;

z-index:10;
}

.arrow-left{
left:10px;
}

.arrow-right{
right:10px;
}

/* ================= CENTER VIEW ================= */

.center-view{

flex:1;

display:flex;
flex-direction:column;

align-items:center;
justify-content:center;

gap:25px;
}

.center-view h2{

letter-spacing:1px;

text-shadow:

0 0 10px rgba(0,255,255,0.7);
}

/* ================= VIDEO CONTROLS ================= */

.video-controls{

display:flex;

gap:12px;

flex-wrap:wrap;
}

.video-controls input{

padding:10px;

border-radius:8px;

border:none;

width:260px;

outline:none;
}

.detect-btn{

padding:10px 16px;

border:none;

border-radius:8px;

cursor:pointer;

font-weight:500;

background:#0ff;

transition:0.3s;
}

.detect-btn:hover{

box-shadow:0 0 12px #0ff;

transform:scale(1.05);
}

/* ================= BACK BUTTON ================= */

.back-btn{

padding:8px 14px;

border:none;

border-radius:8px;

cursor:pointer;

background:#0ff;

font-weight:500;
}

/* ================= CAMERA WINDOW ================= */

.camera-box{

width:780px;
height:450px;

background:black;

border-radius:14px;

display:flex;
align-items:center;
justify-content:center;

border:1px solid rgba(0,255,255,0.3);

box-shadow:

0 0 50px rgba(0,255,255,0.25);

font-size:15px;

color:#777;
}

/* ================= ALERT PANEL ================= */

.alerts{

width:300px;

padding:20px;

border-left:1px solid rgba(255,255,255,0.1);

display:flex;

flex-direction:column;

gap:10px;

backdrop-filter:blur(10px);
}

.alerts h3{

margin-top:20px;

color:#0ff;

font-size:16px;
}

.alert{

background:#0b0e16;

padding:10px;

border-radius:6px;

border-left:3px solid cyan;
}

.telegram{

background:#042;

padding:10px;

border-radius:6px;

border-left:3px solid lime;

color:#aaffcc;
}

/* ================= MOBILE ================= */

@media(max-width:900px){

.layout{

flex-direction:column;

gap:25px;
}

.semicircle-wrapper{

height:320px;
}

.semicircle{

width:500px;
height:500px;

left:-250px;
}

.camera-box{

width:92%;
height:240px;
}

.alerts{

width:100%;

border-left:none;

border-top:1px solid rgba(255,255,255,0.1);
}

}