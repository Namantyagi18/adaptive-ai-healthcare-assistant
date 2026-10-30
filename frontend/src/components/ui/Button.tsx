import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost' | 'emerald';
type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends HTMLMotionProps<'button'> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  icon,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles =
    'relative inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed select-none';

  const sizeStyles: Record<ButtonSize, string> = {
    sm: 'text-xs px-3 py-1.5 gap-1.5',
    md: 'text-sm px-4 py-2.5 gap-2',
    lg: 'text-base px-6 py-3.5 gap-2.5',
  };

  const variantStyles: Record<ButtonVariant, string> = {
    primary:
      'bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-semibold shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/35 focus:ring-cyan-400 border border-cyan-400/30',
    secondary:
      'bg-slate-800 hover:bg-slate-700 text-slate-100 border border-slate-700/80 shadow-md hover:border-slate-600 focus:ring-slate-500',
    danger:
      'bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white font-semibold shadow-lg shadow-rose-600/25 focus:ring-rose-500 border border-rose-500/30',
    emerald:
      'bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-semibold shadow-lg shadow-emerald-500/20 focus:ring-emerald-400 border border-emerald-400/30',
    outline:
      'bg-transparent hover:bg-cyan-500/10 text-cyan-400 border border-cyan-500/40 hover:border-cyan-400 focus:ring-cyan-400',
    ghost:
      'bg-transparent hover:bg-slate-800/80 text-slate-300 hover:text-white focus:ring-slate-600',
  };

  return (
    <motion.button
      whileHover={disabled || isLoading ? undefined : { scale: 1.02 }}
      whileTap={disabled || isLoading ? undefined : { scale: 0.98 }}
      disabled={disabled || isLoading}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <>
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Loading...</span>
        </>
      ) : (
        <>
          {icon && <span className="inline-flex shrink-0">{icon}</span>}
          <span>{children}</span>
        </>
      )}
    </motion.button>
  );
};
