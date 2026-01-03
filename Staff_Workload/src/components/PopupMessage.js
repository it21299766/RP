/**
 * PopupMessage Component
 * 
 * This component displays temporary popup messages for user feedback.
 * It supports different message types (success, error, delete) with appropriate icons.
 * 
 * Features:
 * - Auto-dismiss after specified duration
 * - Manual close button
 * - Type-specific styling and icons
 * - Smooth animations
 * - Non-blocking overlay
 * 
 * Props:
 * - message: String - Message text to display
 * - type: String - Message type: 'success', 'error', or 'delete'
 * - onClose: Function - Callback called when message is closed (required)
 * - duration: Number - Auto-dismiss duration in milliseconds (default: 3000)
 * 
 * Message Types:
 * - 'success': Green styling with checkmark icon (for successful operations)
 * - 'error': Red styling with error icon (for validation errors, permission denials)
 * - 'delete': Red styling with trash icon (for deletion confirmations)
 * 
 * Usage:
 * Used throughout the application to provide user feedback for:
 * - Successful CRUD operations
 * - Validation errors
 * - Permission denials
 * - Deletion confirmations
 * 
 * Dependencies:
 * - None (standalone component)
 */
// Import React and useEffect hook for side effects
import React, { useEffect } from 'react';
// Import CSS styles for popup styling
import './PopupMessage.css';

// Component function with props destructuring and default duration value
const PopupMessage = ({ message, type, onClose, duration = 3000 }) => {
  // useEffect hook runs when component mounts or dependencies change
  useEffect(() => {
    // Only set timer if duration is greater than 0 (allows disabling auto-dismiss)
    if (duration > 0) {
      // Set timeout to automatically close popup after specified duration
      const timer = setTimeout(() => {
        // Call onClose callback to close the popup
        onClose();
      }, duration);
      // Cleanup function: clear timeout if component unmounts before timer completes
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]); // Dependencies: re-run effect if duration or onClose changes

  // Return JSX structure for popup message
  return (
    // Main container with dynamic class based on message type (success, error, delete)
    <div className={`popup-message popup-${type}`}>
      {/* Content wrapper for popup elements */}
      <div className="popup-content">
        {/* Icon container */}
        <div className="popup-icon">
          {/* Conditional rendering: show checkmark icon for success messages */}
          {type === 'success' && (
            // SVG checkmark icon (green check)
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Path defining checkmark shape */}
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
            </svg>
          )}
          {/* Conditional rendering: show trash icon for delete messages */}
          {type === 'delete' && (
            // SVG trash/delete icon
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Path defining trash can shape */}
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
            </svg>
          )}
        </div>
        {/* Text container displaying the message content */}
        <div className="popup-text">{message}</div>
        {/* Close button that calls onClose when clicked */}
        <button className="popup-close" onClick={onClose}>
          {/* SVG X icon for close button */}
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Path defining X shape (two diagonal lines) */}
            <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

// Export component as default for use in other files
export default PopupMessage;



