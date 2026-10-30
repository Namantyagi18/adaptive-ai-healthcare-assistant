import React from 'react';
import { motion } from 'framer-motion';

interface VoiceWaveformProps {
  isActive: boolean;
  barsCount?: number;
  color?: string;
}

export const VoiceWaveform: React.FC<VoiceWaveformProps> = ({
  isActive,
  barsCount = 18,
  color = 'bg-cyan-400',
}) => {
  const bars = Array.from({ length: barsCount });

  return (
    <div className="flex items-center justify-center gap-1.5 h-16 px-4">
      {bars.map((_, i) => {
        // Varying initial heights
        const minHeight = 8;
        const maxHeight = isActive ? 48 : 8;

        return (
          <motion.div
            key={i}
            className={`w-1 rounded-full ${color}`}
            animate={
              isActive
                ? {
                    height: [
                      minHeight,
                      Math.max(12, Math.random() * maxHeight),
                      minHeight,
                    ],
                  }
                : { height: minHeight }
            }
            transition={
              isActive
                ? {
                    repeat: Infinity,
                    duration: 0.4 + (i % 5) * 0.1,
                    ease: 'easeInOut',
                    delay: (i * 0.05) % 0.3,
                  }
                : { duration: 0.2 }
            }
          />
        );
      })}
    </div>
  );
};

