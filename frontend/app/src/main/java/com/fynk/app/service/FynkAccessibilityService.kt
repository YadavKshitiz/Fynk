package com.fynk.app.service

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent

class FynkAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // To be implemented
    }

    override fun onInterrupt() {
        // To be implemented
    }
}
