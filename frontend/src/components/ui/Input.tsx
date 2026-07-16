import type { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input = ({ label, error, id, className = '', ...rest }: InputProps) => {
  const inputId = id ?? label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={inputId} className="text-[13px] font-semibold text-ink">
        {label}
      </label>
      <input
        id={inputId}
        className={`rounded border bg-surface px-[13px] py-[11px] text-sm text-ink focus:border-primary focus:outline-none focus:ring-[3px] focus:ring-primary-50 ${
          error ? 'border-danger' : 'border-border'
        } ${className}`}
        aria-invalid={error !== undefined}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...rest}
      />
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-danger">
          {error}
        </p>
      )}
    </div>
  );
};
