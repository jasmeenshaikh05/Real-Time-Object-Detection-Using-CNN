import { motion } from "framer-motion";

function Sidebar() {

  const modules = [
    "Object Detection",
    "Hazard Detection",
    "Crowd Monitoring",
    "Sign Translator"
  ];

  return (
    <div className="bg-dark text-light p-3 vh-100">

      <h3 className="text-center mb-4">🐆 PantherAI</h3>

      {modules.map((module, index) => (
        <motion.div
          key={index}
          whileHover={{ scale: 1.08, boxShadow:"0px 0px 15px #00f2ff"}}
          whileTap={{ scale:0.95 }}
          className="bg-secondary p-3 mb-3 rounded text-center"
          style={{cursor:"pointer"}}
        >
          {module}
        </motion.div>
      ))}

    </div>
  );
}

export default Sidebar;