
import React from 'react';

export const SparklesIcon: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
    <path d="M18 10h.01" />
    <path d="M12 18h.01" />
    <path d="M21 15h.01" />
    <path d="M21 9h.01" />
    <path d="M9 21h.01" />
    <path d="M3 15h.01" />
    <path d="M6 12h.01" />
    <path d="M3 9h.01" />
  </svg>
);
