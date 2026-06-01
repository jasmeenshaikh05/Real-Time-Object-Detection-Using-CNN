import React,{useState} from "react";
import LoadingScreen from "./components/LoadingScreen";
import Dashboard from "./components/Dashboard";

function App(){

  const [loading,setLoading] = useState(true);

  return(

    <>
      {loading
        ? <LoadingScreen onFinish={()=>setLoading(false)}/>
        : <Dashboard/>
      }
    </>

  );

}

export default App;