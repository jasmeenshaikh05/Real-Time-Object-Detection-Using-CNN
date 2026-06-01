import { motion } from "framer-motion";

function CameraFeed() {

  return (

    <motion.div
      className="bg-dark p-3 rounded"
      initial={{opacity:0, y:-20}}
      animate={{opacity:1, y:0}}
      transition={{duration:0.5}}
      style={{
        boxShadow:"0px 0px 20px rgba(0,255,255,0.3)"
      }}
    >

      <h5>📷 Live Camera Feed</h5>

      <img
        src="http://localhost:5000/video_feed"
        alt="camera"
        width="100%"
      />

    </motion.div>

  );

}

export default CameraFeed;