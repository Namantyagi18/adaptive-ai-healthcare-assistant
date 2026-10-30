import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface CardProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode;
  className?: string;
  glow?: boolean;
  hoverEffect?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  glow = false,
  hoverEffect = false,
  ...props
}) => {
  return (
    <motion.div
      whileHover={hoverEffect ? { y: -4, transition: { duration: 0.2 } } : undefined}
      className={`relative rounded-2xl bg-slate-900/70 backdrop-blur-xl border border-slate-800/80 p-6 shadow-xl transition-shadow ${
        glow ? 'border-cyan-500/30 shadow-cyan-500/10 shadow-2xl' : ''
      } ${hoverEffect ? 'hover:border-slate-700 hover:shadow-2xl' : ''} ${className}`}
      {...props}
    >
      {glow && (
        <div className="absolute -inset-px rounded-2xl bg-gradient-to-r from-cyan-500/20 via-teal-500/10 to-transparent pointer-events-none opacity-50" />
      )}
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
};

