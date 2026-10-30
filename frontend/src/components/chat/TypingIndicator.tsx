import React from 'react';
import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start gap-3 my-4">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 text-slate-950 shadow-md shadow-cyan-500/20">
        <Activity className="w-4 h-4 animate-spin" />
      </div>
      <div className="rounded-2xl bg-slate-900/90 border border-slate-800 px-4 py-3 shadow-md max-w-sm">
        <div className="flex items-center gap-2 mb-1.5 text-xs text-cyan-400 font-medium">
          <span>Consulting verified medical guidelines...</span>
        </div>
        <div className="flex items-center gap-1.5">
          <motion.span
            animate={{ scale: [1, 1.4, 1] }}
            transition={{ repeat: Infinity, duration: 0.8, delay: 0 }}
            className="h-2 w-2 rounded-full bg-cyan-400"
          />
          <motion.span
            animate={{ scale: [1, 1.4, 1] }}
            transition={{ repeat: Infinity, duration: 0.8, delay: 0.2 }}
            className="h-2 w-2 rounded-full bg-teal-400"
          />
          <motion.span
            animate={{ scale: [1, 1.4, 1] }}
            transition={{ repeat: Infinity, duration: 0.8, delay: 0.4 }}
            className="h-2 w-2 rounded-full bg-cyan-300"
          />
        </div>
      </div>
    </div>
  );
};
