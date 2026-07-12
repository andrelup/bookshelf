import { describe, expect, it } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useToast } from './useToast';

describe('useToast', () => {
  it('throws when used outside a ToastProvider', () => {
    expect(() => renderHook(() => useToast())).toThrow(
      'useToast must be used within a ToastProvider',
    );
  });
});
