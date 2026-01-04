/**
 * PopupMessage Component
 * 
 * Displays a temporary notification message that auto-dismisses after a specified duration.
 * Used for success messages, delete confirmations, and other user feedback.
 * 
 * Features:
 * - Auto-dismisses after specified duration (default 3 seconds)
 * - Shows different icons based on message type (success, delete)
 * - Can be manually closed via close button
 * - Styled with CSS for different message types
 * 
 * @param {string} message - The message text to display
 * @param {string} type - Message type: 'success' or 'delete' (determines icon and styling)
 * @param {function} onClose - Callback function called when message is dismissed
 * @param {number} duration - Auto-dismiss duration in milliseconds (default: 3000ms)
 */

import React, { useEffect } from 'react';
import './PopupMessage.css';

const PopupMessage = ({ message, type, onClose, duration = 3000 }) => {
  /**
   * Effect: Auto-dismiss message after specified duration
   * 
   * Sets up a timer that calls onClose() after the duration.
   * If duration is 0 or negative, message stays until manually closed.
   * 
   * Cleanup: Clears timer if component unmounts before duration expires
   */
  useEffect(() => {
    if (duration > 0) {
      // Set timer to auto-close after duration milliseconds
      const timer = setTimeout(() => {
        onClose();
      }, duration);
      
      // Cleanup: Clear timer if component unmounts or duration changes
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  /**
   * Render popup message with icon, text, and close button
   * 
   * Structure:
   * - Container with type-based CSS class (popup-success or popup-delete)
   * - Icon (checkmark for success, trash for delete)
   * - Message text
   * - Close button (X icon)
   */
  return (
    <div className={`popup-message popup-${type}`}>
      <div className="popup-content">
        {/* Icon: Shows checkmark for success, trash icon for delete */}
        <div className="popup-icon">
          {type === 'success' && (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" fill="currentColor"/>
            </svg>
          )}
          {type === 'delete' && (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
            </svg>
          )}
        </div>
        
        {/* Message text */}
        <div className="popup-text">{message}</div>
        
        {/* Close button: Allows manual dismissal before auto-dismiss */}
        <button className="popup-close" onClick={onClose}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default PopupMessage;

